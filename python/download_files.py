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
    :return: Map from sample name to URL of its VCF file.
    :rtype: collections.OrderedDict
    """
    sample_to_vcf = OrderedDict()

    with open(file, "r") as f:
        idx = json.load(f)
        for i in idx:
            if "filename" in idx[i]:
                sample = idx[i]["vcf_sample"]
                vcf = idx[i]["filename"]
                assert re.search(sample, vcf),\
                    f"vcf_sample does not match filename at {i}"
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
    help="Local directory to store VCF files"
)
def download_files_from_ftp(json_file, ftp_site, out_dir):
    sample_to_vcf = parse_json_file(json_file)
    for sample_name, vcf_file in sample_to_vcf.items():
        vcf_src_file = ftp_site + vcf_file
        vcf_dest_file = out_dir + sample_name + ".masked.vcf.gz"
        tbi_src_file = vcf_src_file + ".tbi"
        tbi_dest_file = vcf_dest_file + ".tbi"
        urllib.request.urlretrieve(vcf_src_file, vcf_dest_file)
        urllib.request.urlretrieve(tbi_src_file, tbi_dest_file)


if __name__ == "__main__":
    #ftp_site = "http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reproducibility/"
    #json_file = "cryptic-index_February2022.json"
    download_files_from_ftp()
