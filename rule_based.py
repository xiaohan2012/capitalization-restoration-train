import argparse
from puls_util import separate_title_from_body
from label import get_label


def output_labels(doc_ids, good_corpus_dir, bad_corpus_dir):
    """
    Output the correct labels of the given documents specified in doc_ids
    under bad_corpus_dir
    """
    for doc_id in doc_ids:
        titles, _ = separate_title_from_body(
            good_corpus_dir + '/{}.auxil'.format(doc_id),
            good_corpus_dir + '/{}.paf'.format(doc_id)
        )
        
        assert len(titles) == 1
        good_title = titles[0]
        labels = [get_label(w['token']) for w in good_title['features']]

        # print(bad_corpus_dir + '/{}.labels'.format(doc_id))
        
        with open(bad_corpus_dir + '/{}.labels'.format(doc_id), 'w') as f:
            f.write(' '.join(labels))
    

def main():
    parser = argparse.ArgumentParser(description='Output labels')
    parser.add_argument('--doc_id_path', help="doc ids path", type=str, required=True)
    parser.add_argument('--good_dir', help="good corpus dir", type=str, required=True)
    parser.add_argument('--bad_dir', help="bad corpus dir", type=str, required=True)
    
    args = parser.parse_args()
    
    with open(args.doc_id_path) as f:
        doc_ids = [l.strip() for l in f]
        
    output_labels(doc_ids, args.good_dir, args.bad_dir)

if __name__ == '__main__':
    main()
