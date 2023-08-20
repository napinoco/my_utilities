import regex
import streamlit as st
from graphviz import Digraph


def analyze(query_script: str) -> dict:
    comment_pattern = r'--.*\n|#.*\n|/\*([^*]|\*[^/])*\*/'
    query_script = regex.sub(comment_pattern, '', query_script)

    cte_pattern = r'(?:with|,)\s*(\w+)\s+as\s*(?<rec>\((?:[^\(\)]+|(?&rec))*\))'
    ctes = regex.finditer(cte_pattern, query_script, regex.IGNORECASE)
    queries = {cte.group(1): cte.group(2) for cte in ctes}

    main_pattern = r'\)[;\s]*select' if any(queries) else r'select'
    start_main = regex.search(main_pattern, query_script, regex.IGNORECASE).span()[0] + 1
    queries['main'] = query_script[start_main:].strip()

    ref_pattern = r'(?:from|join)\s+([`.\-\w]+)'
    dependencies = dict()
    for name, script in queries.items():
        refs = regex.findall(ref_pattern, script, regex.IGNORECASE)
        dependencies[name] = [ref for ref in refs]

    return dependencies


def draw_graph(dependencies: dict):
    # draw graph
    g = Digraph()
    g.attr('node', shape='box')
    g.attr('graph', rankdir='LR')
    with g.subgraph(name='queries') as c:
        c.attr(color='blue', label='queries')
        for name, refs in dependencies.items():
            for ref in refs:
                c.node(name, style='bold, filled' if name=='main' else 'solid, filled', fillcolor='#FFFFFF' if name=='main' else '#80CBC4')
                c.node(ref, style='solid, filled', fillcolor='#81C784' if '.' in ref else '#80CBC4')
                c.edge(ref, name)
    st.graphviz_chart(g)


def write_mermaid(dependencies: dict) -> str:
    mermaid_script = f'flowchart LR\n'
    for name, refs in dependencies.items():
        for ref in refs:
            mermaid_script += f'    {ref} --> {name}\n'
    return mermaid_script


def extract_input(dependencies: dict) -> str:
    in_table = set()
    out_table = set()
    for name, refs in dependencies.items():
        out_table.update({name})
        in_table.update(set(refs))

    tmp = ''
    for t in sorted(list(in_table - out_table)):
        tmp += f'{t}\n'
    return tmp


if __name__ == '__main__':
    query_script = st.text_area('Enter SQL script.', height=400)
    try:
        ...
    except:
        st.subheader('Check and modify script')

    dependencies = analyze(query_script)
    draw_graph(dependencies)
    mermaid = write_mermaid(dependencies)
    st.text_area('mermaid', value=mermaid, height=200)
    in_table = extract_input(dependencies)
    st.text_area('input', value=in_table, height=200)