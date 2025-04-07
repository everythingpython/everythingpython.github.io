def invoke_llm(sys_prompt=None, user_prompt=None, provider=None):

    if provider == "azure":
        from .clients.azure_client import AzureClient
        client_obj = AzureClient()
    else:
        from .clients.openai_client import OpenAIClient
        client_obj = OpenAIClient()
    client_ = client_obj.client
    model_ = client_obj.model

    if not sys_prompt:
        sys_prompt = "You are an AI assistant. Chat with the user in a casual manner. "

    messages=[
        {"role": "system", "content":sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client_.chat.completions.create(
                    model=model_,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=2048,
                    top_p=0.95,
                    seed=11,
                    frequency_penalty=0.3,
                    presence_penalty=0
                )
    
    llm_response = response.choices[0].message.content
    print(llm_response)

    return llm_response