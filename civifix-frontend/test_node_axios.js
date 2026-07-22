import axios from 'axios';
const BASE_URL = "http://127.0.0.1:8000/api/v1";
async function test() {
    try {
        await axios.post(`${BASE_URL}/auth/register`, {
            email: "testuser@example.com",
            password: "password123",
            full_name: "Test User",
            role: "CITIZEN",
            phone: "1234567890"
        });
    } catch(e) {
        console.error("Reg Error:", e.response ? e.response.data : e.message);
    }
}
test();
