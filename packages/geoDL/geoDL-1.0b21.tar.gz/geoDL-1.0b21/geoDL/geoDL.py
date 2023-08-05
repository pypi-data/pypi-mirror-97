#!/usr/bin/env python3
"""
Download data from the ENA website using a GSE geo accession number, ENA study accession number or
metadata spreadsheet.

url: https://github.com/jduc/geoDL
author: Julien Duc <julien_dot_duc_dot_0_at_gmail_dot_com>
"""
import sys
import os
import re
import argparse
import csv
from subprocess import call
import requests
import bs4
from bs4 import BeautifulSoup
from colorama import Fore
from six.moves.urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from csv import reader


__version__ = "v1.0.b21"
logo = """
################################################################################
               ___  _
  __ _ ___ ___|   \| |
 / _` / -_) _ \ |) | |__
 \__, \___\___/___/|____|
 |___/                   {}

################################################################################
""".format(
    __version__
)


class SmartFormatter(argparse.HelpFormatter):
    """Quick hack for formatting helper of argparse with new lines"""

    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def raiseError(errormsg):
    print("\n" + Fore.RED + errormsg + Fore.RESET)
    sys.exit(1)


def get_args():
    """Parse and return all arguments"""
    parser = argparse.ArgumentParser(
        description="""Download fastq from The European Nucleotide Archive (ENA)
                                     <http://www.ebi.ac.uk/ena> website using a GSE geo
                                     <http://www.ncbi.nlm.nih.gov/geo/info/seq.html> accession, ENA
                                     study accession or a metadata file from ENA""",
        formatter_class=SmartFormatter,
        epilog="Made with <3 at the batcave",
    )
    parser.add_argument(
        "mode", choices=["geo", "meta", "ena", "prefetch"], help="Which mode the program runs."
    )
    parser.add_argument(
        "inputvalue",
        metavar="GSE|metadata|ENA|prefetch",
        help="""R|geo:  GSE accession number, eg: GSE13373
      Map the GSE accession to the ENA study accession and fetch the metadata from ENA.

meta: Use metadata file instead of fetching it on ENA website (bypass GEO)
      Meta data should include at minima the following columns: ['Fastq files
      (ftp)', 'Submitter's sample name']

ena:  ENA study accession number, eg: PRJEB13373
      Fetch the metadata directely on the ENA website

prefetch: Use NCBI prefetch (on NCBI server) to download the data, bypass the ENA website
      entirely. This gives back SRA files - use NCBI tools for conversion. """,
    )
    parser.add_argument(
        "--ascp",
        action="store_true",
        help="Use Aspera for the download (requires an already configured aspera)",
    )
    parser.add_argument(
        "--asperakey",
        type=str,
        default="/etc/asperaweb_id_dsa.openssh",
        help="The ssh key of apsera (/etc/asperaweb_id_dsa.openssh)",
    )
    parser.add_argument(
        "--samples",
        type=str,
        default=[],
        nargs="*",
        help="Space separated list of GSM samples to download. For ENA mode, subset the metadata",
    )
    parser.add_argument(
        "--colname",
        type=str,
        default="geo_name",
        help="Name of the column to use in the metadata file to name the samples",
    )
    parser.add_argument(
        "--ncbipath",
        help="Path to the SRA folder of NCBI files default: ~/ncbi/public/sra",
        default="~/ncbi/public/sra/",
        type=str
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Don't actually download anything, just print the ncftp cmds",
    )
    return parser.parse_args()


def get_metadata(args):
    """Get the metadata. If geo mode, search on ENA website, if ENA, directely take
    from the ENA website. Also return the mapping between GEO and ENA naming"""
    map_dict = {}
    if args.mode == "geo":
        print("Getting correspondance table from GEO...")
        geo_url = f"https://www.ncbi.nlm.nih.gov/geo/browse/?view=samples&display=500&series={args.inputvalue.replace('GSE', '')}"
        try:
            geo_soup = BeautifulSoup(urlopen(geo_url).read(), "html.parser")
        except URLError:
            raiseError(" > ERROR: Could not reach GEO website... exiting!")

        try:
            npages = int(geo_soup.find("span", attrs={"id": "page_cnt"}).text)
        except AttributeError:  # there is no pages
            npages = 1
        for page in range(1, npages+1):
            print(
                Fore.YELLOW
                + f"..Parsing page {page}..."
                + Fore.RESET
            )
            geo_url = f"https://www.ncbi.nlm.nih.gov/geo/browse/?view=samples&display=500&page={page}&series={args.inputvalue.replace('GSE', '')}"
            geo_soup = BeautifulSoup(urlopen(geo_url).read(), "html.parser")
            geo_table = geo_soup.find("table", attrs={'id':'geo_data'})
            thead = geo_table.find('thead')
            tbody = geo_table.find('tbody')
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                if tds[0].text.strip() == "Filter":
                    continue
                map_dict[tds[0].text.strip()] = tds[1].text.strip()
        print(
            Fore.GREEN
            + " > Found {} samples on GEO page...".format(len(map_dict))
            + Fore.RESET
        )
        url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={args.inputvalue}"
        geo_soup = BeautifulSoup(urlopen(url).read(), "html.parser")
        projurl = [url for url in geo_soup.find_all("a") if "PRJ" in url.get_text()][0]
        prj = projurl.text
        metafile = f"metadata_{args.inputvalue}.xls"
        urlretrieve(
            f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={prj}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,library_strategy,run_alias,fastq_ftp,fastq_aspera,submitted_ftp,sra_ftp,sample_alias&format=tsv&download=true",
        metafile)
        new_rows = []
        with open(metafile, "r") as meta:
            for i, row in enumerate(csv.reader(meta, delimiter="\t")):
                if i == 0:
                    new_rows.append([r.strip() for r in row] + ["geo_name"])
                    sample_alias_idx = row.index("sample_alias")
                    run_alias_idx = row.index("run_alias")
                else:
                    r = re.search(r"_(r\d+)", row[run_alias_idx]).group(1)
                    new_rows.append(row + [map_dict[row[sample_alias_idx]] + f"_{r}"])
        with open(metafile, "w") as out:
            metawriter = csv.writer(out, delimiter="\t")
            for row in new_rows:
                metawriter.writerow(row)

        print(Fore.GREEN + " > Metafile retrieved {}!".format(metafile) + Fore.RESET)

    elif args.mode == "ena":
        metafile = "metadata_{}.xls".format(args.inputvalue)
        urlretrieve(
            f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={args.inputvalue}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,library_strategy,run_alias,fastq_ftp,fastq_aspera,submitted_ftp,sra_ftp,sample_alias&format=tsv&download=true",
            metafile)
        print(
            Fore.GREEN
            + " > Metafile retrieved from ENA {}!".format(metafile)
            + Fore.RESET
        )
    elif args.mode == "meta":
        print(
            "\nUsing the {} metadata file ony (bypass GEO)...".format(args.inputvalue)
        )
        metafile = args.inputvalue

    elif args.mode == "prefetch":
        print("Prefetch mode: getting the SRR list...")
        metafile = "metadata_{}.xls".format(args.inputvalue)
        r = requests.get(
            "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}".format(
                gse=args.inputvalue
            )
        )
        geosoup = BeautifulSoup(r.text, "html.parser")
        projurl = [url for url in geosoup.find_all("a") if "PRJ" in url.get_text()][0]
        payload = {"db": "SRA",
                   "term": "{}".format(projurl.get_text()),
                   "retmax": 10000}
        r = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params=payload
        )
        esearchsoup = BeautifulSoup(r.text, "lxml")
        ids = [i.get_text() for i in esearchsoup.idlist.find_all("id")]
        print(Fore.GREEN + "> Found {} entries...".format(len(ids)) + Fore.RESET)
        payload = {"db": "SRA",
                   "id": ','.join(ids)}
        r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
                params=payload)
        efetchsoup = BeautifulSoup(r.text, "lxml")
        exps = efetchsoup.find_all("run_set")
        assert len(exps) == len(ids)
        runs = efetchsoup.find_all("run")
        map_dict = {}
        n_rep = len(set([run["alias"].split("_")[1] for run in runs]))
        with open(metafile, "w") as meta:
            for i, run in enumerate(runs):
                name = run.pool.member["sample_title"]
                if n_rep > 1:
                    suffix = run["alias"].split("_")[1]  # e.g. GSM20202020_r2
                    rename = name
                else:
                    rename = name
                map_dict[run["accession"]] = rename
                if i == 0:
                    header = "\t".join(list(run.attrs.keys()) + \
                                       list(run.pool.member.attrs.keys()) + \
                                       ["paired", "rename"]) + \
                                       "\n"
                    meta.write(header)
                paired = "SE" if len(run.statistics.find_all("read")) == 1 else "PE"
                data = "\t".join(list(run.attrs.values()) + \
                                 list(run.pool.member.attrs.values()) + \
                                 [paired, rename]) + \
                                 "\n"
                meta.write(data)
    return metafile, map_dict


def ena_dl(args, metafile, map_dict):
    """Download the data from ENA using ncftp or ascp, using the metadta the metadata
    """

    # check that the column selected for naming is uniq
    with open(metafile) as f:
        reader = csv.reader(f, delimiter="\t")
        samplenames = []
        for i, row in enumerate(reader):
            if i == 0:
                if args.colname not in row:
                    raiseError(
                        "  > ERROR: Column {col} not in the metadata file "
                        "{meta}".format(col=args.colname, meta=metafile)
                    )
                for j, c in enumerate(row):
                    if c == args.colname:
                        idx = j
            else:
                if row[idx] in samplenames:
                    raiseError(
                        "  > ERROR: Non uniq sample names in the column {col} "
                        "of the meta file {meta}\n".format(
                            col=args.colname, meta=metafile
                        )
                    )
                samplenames.append(row[idx])

    dlsoft = "aspera" if args.ascp else "ncftp"
    print("Starting the downloads with {}\n".format(dlsoft))
    with open(metafile) as f, open("geoDL.logs", "w") as log:
        for i, line in enumerate(f):
            if i == 0:
                header = [h.strip() for h in line.split("\t")]
                log.write("{} download log \n".format(args.inputvalue))
                continue
            data = dict(zip(header, [sp.strip() for sp in line.split("\t")]))
            try:
                if dlsoft == "aspera":
                    data_urls = data["fastq_aspera"].split(";")
                else:
                    data_urls = data["fastq_ftp"].split(";")
            except KeyError:
                raiseError(
                    "  > ERROR: Fastq urls (ftp/aspera) are not in the metadata, \
                           make sure to add the column and try again."
                )
            gsm = data["sample_alias"]
            samplename = data[args.colname].replace(" ", "_")
            if len(data_urls) == 2:  # paired end
                suffix = ["_R1", "_R2"]
                pair = True
            elif len(data_urls) == 1:  # single end
                suffix = [""]
                pair = False
            else:
                raiseError(" > ERROR: number of urls in fastq url column is unexpected")
            for r, url in enumerate(data_urls):
                outname = samplename + suffix[r] + ".fq.gz"
                print(
                    Fore.GREEN
                    + "\n > Getting {}...\n".format(outname)
                    + 80 * "="
                    + Fore.RESET
                )
                ncftpcmd = [
                    "ncftpget",
                    "-C",
                    "ftp://" + url,
                    outname
                ]
                log.write(" ".join(ncftpcmd) + "\n")
                ascp = os.popen("which ascp").read().strip()
                ascpcmd = [
                    ascp,
                    "-T",
                    "--policy",
                    "high",
                    "-l",
                    "10G",
                    "-i",
                    args.asperakey,
                    "-P",
                    "33001",
                    "-k2",
                    "era-fasp@" + url,
                    outname
                ]
                if args.dry:
                    if args.ascp:
                        print(" ".join(ascpcmd))
                    else:
                        print(" ".join(ncftpcmd))
                else:
                    if args.ascp:
                        try:
                            ret = call(ascpcmd)
                            if ret != 0:
                                print("  > ERROR: ascp returned {}".format(ret))
                                print("  > cmd was: \n{}".format(" ".join(ascpcmd)))
                                sys.exit(1)
                        except FileNotFoundError:
                            raiseError(
                                "  > ERROR: ascp not found, please install and try again !"
                            )
                        log.write(" ".join(ascpcmd) + "\n")
                    else:
                        try:
                            ret = call(ncftpcmd)
                            if ret == 3 and os.path.isfile(outname):
                                print("  > File is there!")
                            elif ret != 0:
                                print("  > ERROR: ncftp returned {}".format(ret))
                                print("  > cmd was: \n{}".format(" ".join(ncftpcmd)))
                        except FileNotFoundError:
                            raiseError(
                                "  > ERROR: ncftp not found, please install and try again !"
                            )
                            sys.exit(1)
                        log.write(" ".join(ncftpcmd) + "\n")


def prefetch_dl(args, metafile, map_dict):
    """Use the NCBI prefetch program to download the data"""
    assert len(set(map_dict.values())) == len(map_dict.keys()), "Non unique sample name"
    with open(metafile) as meta, open("geoDL.logs", "w") as log:
        for n, sample in enumerate(meta):
            sp = sample.strip().split("\t")
            if n == 0:  # header
                continue
            srr = sp[1]
            if args.ascp:
                ascp = os.popen("which ascp").read().strip()
                # cmd = ["prefetch", "-X", "100000000", "-t", "ascp",
                #        "-a", ascp+"|"+args.asperakey, srr]
                cmd = ["prefetch", "-X", "100000000", "-t", "ascp", srr]
            else:
                cmd = ["prefetch", "-X", "100000000", srr]
            log.write(" ".join(cmd) + "\n")
            call(cmd)
            call(["touch", srr])
            call(["mv", os.path.expanduser(args.ncbipath) + "/" + srr + ".sra", map_dict[srr]+".sra"])


def main():
    print(Fore.BLUE + logo + Fore.RESET)
    args = get_args()
    metafile, map_dict = get_metadata(args)
    if args.mode == "prefetch":
        prefetch_dl(args, metafile, map_dict)
    else:
        ena_dl(args, metafile, map_dict)
    print(Fore.BLUE + "\nIt's over, it's done!\n" + Fore.RESET)


if __name__ == "__main__":
    main()
