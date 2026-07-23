async function run() {
  try {
    let token = null;
    const loginRes = await fetch("http://127.0.0.1:8000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "newcit4@example.com" })
    });
    const log1 = await loginRes.json();
    if (loginRes.status === 200 && log1.success) {
        const loginVerifyRes = await fetch("http://127.0.0.1:8000/api/v1/auth/verify", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: "newcit4@example.com", otp: "123456" })
        });
        const d = await loginVerifyRes.json();
        token = d.data.access_token;
    } else {
        const regRes = await fetch("http://127.0.0.1:8000/api/v1/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: "newcit4@example.com", name: "Test Cit", mobile_number: "1234567890", district: "Some District", password: "pwd", address: "abc" })
        });
        
        const verifyRes = await fetch("http://127.0.0.1:8000/api/v1/auth/verify-register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: "newcit4@example.com", otp: "123456" })
        });
        const verifyData = await verifyRes.json();
        token = verifyData.data.access_token;
    }

    console.log("Token received");

    const form = new FormData();
    form.append("ward_id", "60d5ecb8b392d21234567890"); 
    form.append("complaint_type", "OTHER");
    form.append("description", "Garbage hasn't been collected for a week");
    form.append("priority", "MEDIUM");
    form.append("latitude", "12.9716");
    form.append("longitude", "77.5946");
    form.append("address", "123 MG Road");

    const response = await fetch("http://127.0.0.1:8000/api/v1/complaints/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: form
    });
    
    console.log("Submit Status:", response.status);
    console.log("Submit Response:", await response.text());
  } catch (err) {
    console.log("Error:", err);
  }
}
run();
