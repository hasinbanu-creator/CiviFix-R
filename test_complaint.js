const axios = require("axios");

async function run() {
  try {
    // login
    const login = await axios.post("http://127.0.0.1:8000/api/v1/auth/login", {
      email: "citizen@example.com"
    });
    console.log("Login OTP sent");
    
    // verify
    const verify = await axios.post("http://127.0.0.1:8000/api/v1/auth/verify", {
      email: "citizen@example.com",
      otp: "123456"
    });
    const token = verify.data.data.access_token;
    console.log("Token:", token.substring(0, 20) + "...");

    // create complaint
    const FormData = require('form-data');
    const form = new FormData();
    form.append("ward_id", "60d5ecb8b392d21234567890"); // Example Object ID
    form.append("complaint_type", "GARBAGE");
    form.append("description", "Garbage hasn't been collected for a week");
    form.append("priority", "MEDIUM");
    form.append("latitude", "12.9716");
    form.append("longitude", "77.5946");
    form.append("address", "123 MG Road");

    const response = await axios.post("http://127.0.0.1:8000/api/v1/complaints/", form, {
      headers: {
        Authorization: `Bearer ${token}`,
        ...form.getHeaders()
      }
    });
    console.log("Success:", response.data);
  } catch (err) {
    console.log("Error:", err.response ? JSON.stringify(err.response.data, null, 2) : err.message);
  }
}
run();
