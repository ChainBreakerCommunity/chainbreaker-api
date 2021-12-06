from client import ChainBreakerClient

endpoint = "https://chainbreaker-ibm-grumpy-gecko-lm.mybluemix.net/"
#endpoint = ""
client = ChainBreakerClient(endpoint)
print(client.get_status())
print(client.login())

ads = client.get_ads(language = "spanish", website = "skokka")
print(ads.head(10))

# Get glossary.
glossary = client.get_glossary(domain="sexual")
print(glossary.head(10))