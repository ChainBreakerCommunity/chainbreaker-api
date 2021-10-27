def return_html(server_user, server_password, query):
    html_file = """
    <!DOCTYPE html>
    <head>
        <title>Neovis.js Simple Example</title>
            <style type="text/css">
                html, body {
                    font: 16pt arial;
                }

                #viz {
                    width: 2048px;
                    height: 1080px;
                    border: 1px solid lightgray;
                    font: 22pt arial;
                }
            </style>
    </head>
    
    <script type="text/javascript">

        var viz;

        function draw() {
            var config = {
                container_id: "viz",
                server_url: "bolt://localhost:7687",
                server_user: '""" + server_user + """',
                server_password: '""" + server_password + """',
                labels: {
                    "Character": {
                        "caption": "name",
                        "size": "pagerank",
                        "community": "community",
                        "title_properties": [
                            "name",
                            "pagerank"
                        ]
                    }
                },
                relationships: {
                    "INTERACTS": {
                        "thickness": "weight",
                        "caption": false
                    }
                },
                initial_cypher: '""" + query + """'
            };

            viz = new NeoVis.default(config);
            viz.render();
        }
    </script>
    <body onload="draw()">
        <div id="viz"></div>
        <script src="https://cdn.neo4jlabs.com/neovis.js/v1.5.0/neovis.js"></script>
    </body>  
    </html>
    """
    return html_file

def get_graph_query(community):
    first_node = community[0]
    query = """
    MATCH (a: Ad)-[r1:HAS_RELATION]-(b:Ad)
    MATCH (b:Ad)-[r2:HAS_DATE]-(d:Date)
    MATCH (b:Ad)-[r3:HAS_PHONE]-(p:Phone)
    MATCH (b:Ad)-[r4:HAS_CITY]-(c:City)
    WHERE a.id_ad = {id_ad}
    RETURN *
    """.format(id_ad = first_node)
    query = query.replace("\n", " ")
    return query

def generate_community_graph(server_user, server_password, community):
    query = get_graph_query(community)
    html = return_html(server_user, server_password, query)
    file_path = "communities/graph_" + str(community[0]) + ".html"
    file = open(file_path, "w")
    file.write(html)
    file.close()
    return file_path