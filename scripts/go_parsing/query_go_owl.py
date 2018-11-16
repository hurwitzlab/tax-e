#! /usr/bin/env python3

from SPARQLWrapper import SPARQLWrapper, JSON #to perform web sparql queries
import rdflib                 #to query using the rdflib module
import rdfextras             #to query using the rdflib module
import rdflib.graph as g    #to query using the rdflib module
rdfextras.registerplugins() # so we can Graph.query()
import sys                  #to deal with input args
import re                   #to filter files using regex
import argparse             #to parse command line args

########################################################################

'''
example usage
./query_go_owl.py -p http://purl.obolibrary.org/obo/GO_0055114 -e 1 -i 0

-e: 0 for subClassOf, 1 for subClassOf+
-i 0 not to include original purl, 1 to include original purl
'''

def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-p',
        '--purl',
        help='obo purl for which to find subclasses',
        metavar='str',
        type=str)

    parser.add_argument(
        '-e',
        '--extend',
        help='Bool flag for whether or not to extend to subclasses+ of the original purl',
        metavar='int',
        type=int,
        default=0)

    parser.add_argument(
        '-i',
        '--include',
        help='Bool flag for whether or not to include the original purl in the list of subclasses',
        metavar='int',
        type=int,
        default=0)


    return parser.parse_args()

########################################################################
# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    in_arg = args.purl
    extend = args.extend
    include = args.include

    # Put together a sparql query from pieces.

    # Put together the PREFIX block:
    def prefix_func():
        prefix_list = ['obo: <http://purl.obolibrary.org/obo/>', 'rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>', 'rdfs: <http://www.w3.org/2000/01/rdf-schema#>', 'owl: <http://www.w3.org/2002/07/owl#>', 'html: <http://tools.ietf.org/html/>']
        insert_prefix = ' \nPREFIX '
        return ('PREFIX ' + insert_prefix.join(prefix_list) + '\n' )

    # Put together a select block
    #takes the query and a bool for whether or not to add a distinct
    def select_func(variables, distinct):
        insert_p = ' ?'
        if distinct == 1:
            return ('SELECT DISTINCT ?' + insert_p.join(variables) + '\n' )
        else:
            return ('SELECT ?' + insert_p.join(variables) + '\n')

    # Put together a WHERE clause which will only query for subclasses+ of a given input class
    def where_subclass_query_func(input_class):
        if extend == 0:
            return 'WHERE {' + '?s rdfs:subClassOf <' + str(input_class) + '> . } \n'
        else:
            return 'WHERE {' + '?s rdfs:subClassOf+ <' + str(input_class) + '> . } \n'


    #put together a sparql query string which will query for subclasses of a
    #given input class
    def subclass_query_function(input_class):
        function_list = [prefix_func(), select_func(['s'], 1), where_subclass_query_func(input_class)]
        return ''.join(function_list)

    #call the function to query for the subclass of the in_arg
    query_for_subclasses = subclass_query_function(in_arg)

    #make a graph object
    graph = g.ConjunctiveGraph()

    #parse the envopolar network
    graph.parse('/Users/kai/Desktop/software/go.owl.ttl', format='ttl')

    #submit the query for subclasses
    results = graph.query(query_for_subclasses)

    #save the results to a file with the name of the input purl
    namestring = str(in_arg)
    #remove the http://purl.obolibrary.org/obo/ from the input file.
    namestring = re.sub('http://purl.obolibrary.org/obo/', '', namestring)
    namestring = re.sub('http://purl.unep.org/sdg/', '', namestring)
    #make the file name to write to
    outstring = 'subclasses_of_' + namestring + '.txt'

    #write out to outfile: query_for_subclasses_of_out.txt
    f = open(namestring, 'w')
    for row in results:
       f.write( "%s\n" % row)

    #
    # #write out to outfile: query_for_subclasses_of_out.txt
    # f = open(outstring, 'w')
    #
    # #add input string to list
    # if include != 0:
    #     f.write(str(in_arg) + '\n')
    # #write each PURL fetched in query to outfile.
    # for res in results["results"]["bindings"] :
    #     f.write(res['s']['value'] + '\n')

# --------------------------------------------------
if __name__ == '__main__':
    main()











#!/usr/bin/python

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib                 #to query using the rdflib module
import rdfextras               #to query using the rdflib module
import rdflib.graph as g       #to query using the rdflib module
rdfextras.registerplugins() # so we can Graph.query()
import sys                    #to deal with input args
import fileinput             #to input files
import re                   #to filter files using regex
import unicodedata #to convert literals to strings

########################################################################
# Put together a sparql query from pieces.

# Put together the PREFIX block:
def prefix_func():
    prefix_list = ['obo: <http://purl.obolibrary.org/obo/>', 'rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>', 'rdfs: <http://www.w3.org/2000/01/rdf-schema#>', 'owl: <http://www.w3.org/2002/07/owl#>', 'html: <http://tools.ietf.org/html/>']
    insert_prefix = ' \nPREFIX '
    return ('PREFIX ' + insert_prefix.join(prefix_list) + '\n' )

# Put together a select block
#takes the query and a bool for whether or not to add a distinct
def select_func(variables, distinct):
    insert_p = ' ?'
    if distinct == 1:
        return ('SELECT DISTINCT ?' + insert_p.join(variables) + '\n' )
    else:
        return ('SELECT ?' + insert_p.join(variables) + '\n')

def from_func():
    return 'FROM <envoPolarttl.owl>\n'

# Put together a WHERE clause which will only query for subclasses+ of a given input class
def where_subclass_query_func():
    return 'WHERE {' + '?s rdf:type owl:Class . } \n'

#put together a sparql query string which will query for subclasses of a
#given input class
def subclass_query_function():
    function_list = [prefix_func(), select_func(['s'], 1),from_func(), where_subclass_query_func()]
    return ''.join(function_list)
