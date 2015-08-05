import json
import codecs
from util import get_title_position

def get_title_from_puls_core_output(aux_file_path,
                                    paf_file_path,
                                    main_file_path):
    """
    """
    with codecs.open(aux_file_path, 'r', 'utf8') as aux_f, \
         codecs.open(main_file_path, 'r', 'utf8') as main_f:
        start, end = get_title_position(paf_file_path)
        data = json.loads(aux_f.read())
        titles = []
        for sent in data['sents']:
            if sent['start'] >= start and sent['end'] <= end:
                titles.append(sent)
        return titles
