from importlib.metadata import requires
from typing_extensions import Required
import click
from collections import OrderedDict
import json
import re
import urllib.request


def parse_json_file(file):
    """
    :param str file: JSON file.
    :return: Map from sample name to URL of its regenotyped VCF file.
    :rtype: collections.OrderedDict
    """
    sample_to_vcf = OrderedDict()

    with open(file, "r") as f:
        idx = json.load(f)
        for i in idx:
            if "regenotyped_vcf" in idx[i]:
                sample = idx[i]["vcf_sample"]
                vcf = idx[i]["regenotyped_vcf"]
                assert re.search(sample, vcf),\
                    f"vcf_sample does not match regenotyped_vcf at {i}"
                sample_to_vcf[sample] = vcf

    return sample_to_vcf


@click.command()
@click.option(
    "--json_file", "-j",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="JSON file"
)
@click.option(
    "--ftp_site", "-f",
    type=str,
    required=True,
    help="URL of FTP site"
)
@click.option(
    "--out_dir", "-o",
    type=click.Path(exists=True, dir_okay=True),
    required=True,
    help="Directory to store downloaded VCF files"
)
def download_files_from_ftp(json_file, ftp_site, out_dir):
    sample_to_vcf = parse_json_file(json_file)
    for sample, vcf in sample_to_vcf.items():
        vcf_src_file = ftp_site + vcf
        vcf_dest_file = out_dir + sample + ".regeno.vcf.gz"
        tbi_src_file = vcf_src_file + ".tbi"
        tbi_dest_file = vcf_dest_file + ".tbi"
        urllib.request.urlretrieve(vcf_src_file, vcf_dest_file)
        urllib.request.urlretrieve(tbi_src_file, tbi_dest_file)
        break


if __name__ == "__main__":
    #json_file = "data/cryptic-index_February2022.json"
    #ftp_site = "http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reproducibility/"
    download_files_from_ftp()
