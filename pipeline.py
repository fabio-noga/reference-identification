import Grabber
import Utils
import TextExtraction

# link = input("Link para documento")
# link = "http://www.dgsi.pt/jstj.nsf/954f0ce6ad9dd8b980256b5f003fa814/d0709de8f1e6b3be8025697e004a2120?OpenDocument"
link = "http://www.dgsi.pt/jstj.nsf/954f0ce6ad9dd8b980256b5f003fa814/960d138417b4ee33802588e70049c8c0?OpenDocument"

# Download file
full_data = Grabber.getDataFromLink(link)
clean_full_data = Utils.createJsonSchemaFromRawSchema(full_data)

# Identify References
parsed_data = Utils.getQuotesFromDataByName(clean_full_data)
reference_list = Utils.getOnlyReferencesFromExtractedData(parsed_data)

# Extract information
quotes = TextExtraction.extractQuoteDataFromPhrase(reference_list[0])
print(quotes)
for quote in quotes:
    print(TextExtraction.getQuoteJsonAsIEEE(quote))