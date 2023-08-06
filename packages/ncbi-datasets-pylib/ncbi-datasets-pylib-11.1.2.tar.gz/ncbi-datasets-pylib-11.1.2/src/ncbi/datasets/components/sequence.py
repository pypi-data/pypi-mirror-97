from cachetools import cached, TTLCache
from gffutils.iterators import DataIterator

import logging

logger = logging.getLogger(__name__)

COUNT_CACHE = TTLCache(maxsize=500, ttl=300)


@cached(COUNT_CACHE)
def count_for(fn, filter_str):
    counts = {}
    filt = filter_str.split(',')
    for rec in DataIterator(fn):
        if rec.featuretype not in filt:
            continue
        if rec.featuretype not in counts:
            counts[rec.featuretype] = 0
        counts[rec.featuretype] += 1
    return counts


class Sequence():
    """Exemplar class to extract summary data for assembly sequences.
    """

    def __init__(self, assembly_report, fasta, gff3):
        self._assembly_report = assembly_report
        self._fasta = fasta
        self._gff3 = gff3

    @staticmethod
    def report_header():
        return [
            'Assembly Accession',
            'Assembly Description',
            '# assembly scaffolds',
            'Sequence',
            '# genes',
            '10nt @ 10,000',
            'Sequence defline'
        ]

    def report(self):
        logger.debug('Scan %s for gene count', self._gff3)
        gene_count = count_for(self._gff3, 'gene')
        logger.debug('Gene: %d', gene_count)
        return [
            self._assembly_report.assembly_info.refseq_assm_acc,
            f'...{self._assembly_report.assembly_info.description[-30:]}',
            self._assembly_report.assembly_stats.number_of_scaffolds,
            self._fasta.name,
            gene_count['gene'],
            f'{self._fasta[10000:10010].seq}',
            f'...{self._fasta.description[-30:]}'
        ]

    # Accessors per need in gather_report() above
    def assm_name(self):
        pass

    def assm_acc(self):
        pass

    def seq_deflines(self):
        pass

    def seq_length(self):
        pass

    def feature_count(self):
        pass

    def literal(self):
        pass

    def accver(self):
        pass
