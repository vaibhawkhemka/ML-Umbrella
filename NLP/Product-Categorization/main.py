from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    title: str
    thumbnail: str

@app.post("/api/analyze")
async def analyze(input_data: InputData):
    title = input_data.title
    thumbnail= input_data.thumbnail

    import torch
    from transformers import BertForSequenceClassification, BertTokenizer
    import torch.nn.functional as F

    device = "cpu"
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                            do_lower_case=True)
    encoded_data_test = tokenizer.encode_plus(
    title, 
    add_special_tokens=True, 
    return_attention_mask=True, 
    pad_to_max_length=True, 
    max_length=256, 
    return_tensors='pt'
)

    input_ids_test = encoded_data_test['input_ids']
    attention_masks_test = encoded_data_test['attention_mask']

    batch = (input_ids_test, attention_masks_test)
    batch = tuple(b.to(device) for b in batch)

    inputs = {'input_ids':      batch[0],
          'attention_mask': batch[1],
          }

    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                        num_labels=6,
                                                        output_attentions=False,
                                                        output_hidden_states=False)

    model.to(device)

    model.load_state_dict(torch.load('checkpoints/finetuned_BERT_Kmeans_epoch.model', map_location=torch.device('cpu')))
    
    #model.load_state_dict(torch.load('checkpoints/finetuned_BERT_LDA_epoch.model', map_location=torch.device('cpu')))
    predictions = []
    with torch.no_grad():        
        outputs = model(**inputs)

        logits = outputs[0]
        
        logits = logits.detach().cpu().numpy()
        
        predictions.append(logits)

    softmax_output = F.softmax(torch.tensor(logits), dim=1)

    ### Labelling Results - For LDA
    #map_to_output = {0:"Laptop",1:"Others",2:"Printers",3:"Smartwatch", 4:"Mobile",5:"Desktop"}

    ### Labelling Results - For Kmeans
    map_to_output = {0:"Mobile",1:"Printer",2:"Desktop",3:"Smartwatch", 4:"Others",5:"Laptop"}


    final_dict = {value: prob.item() for prob, value in zip(softmax_output[0], map_to_output.values())}

    max_position = torch.argmax(softmax_output).item()
    Product_Type = map_to_output[max_position]
    Product_Type_conf_score = final_dict[map_to_output[max_position]]
    Other_Possible_Product_Type = final_dict

    # print("Product Type:", Product_Type)
    # print("Product_Type_conf_score:", Product_Type_conf_score)
    # print("Other_Possible_Product_Type:", Other_Possible_Product_Type)

    return {"title": title, "Thumbnail": thumbnail,"product_type": Product_Type,"Product_Type_conf_score": Product_Type_conf_score,"Other_Possible_Product_Type":Other_Possible_Product_Type}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
