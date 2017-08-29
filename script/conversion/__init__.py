# -*- coding: utf-8 -*-

__version__ = "0.1.0"

#from accession import Accession
#from ensembl import Ensembl
#from gpl import GPL
#from history import History
#from homologene import Homologene
#from info import Info
#from merge_info_homologene import InfoWithHomologene
#from swissprot import Swissprot
#from trembl import TREMBL
#from unigene import Unigene
#from vega import Vega

from accession import Accession as accession
import ensembl
import gpl
import history
import homologene
import info
import merge_info_homologene
import swissprot
import trembl
import unigene
import vega
#__all__ = ['Accession', 'Ensembl', 'GPL', 'History', 'Homologene', 'Info', 'InfoWithHomologene', 'Swissprot', 'TREMBL', 'Unigene', 'Vega' ]
__all__ = ['accession', 'ensembl', 'gpl', 'history', 'homologene', 'info', 'merge_info_homologene', 'swissprot', 'trembl', 'unigene', 'vega' ]
