with open("civifix-web/src/constants/endpoints.ts", "r") as f:
    content = f.read()

if "SUBMIT_FEEDBACK" not in content:
    content = content.replace(
        'GET_COMPLAINT: (id: string | number) => `/complaints/${id}`,',
        'GET_COMPLAINT: (id: string | number) => `/complaints/${id}`,\n  SUBMIT_FEEDBACK: (id: string | number) => `/complaints/${id}/feedback`,\n  REOPEN_COMPLAINT: (id: string | number) => `/complaints/${id}/reopen`,'
    )
    with open("civifix-web/src/constants/endpoints.ts", "w") as f:
        f.write(content)
    print("Added SUBMIT_FEEDBACK to endpoints.ts")
