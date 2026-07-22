const form = {
  ward_id: "123",
  complaint_type: "GARBAGE",
  latitude: 12.34,
  longitude: 56.78
}

const formData = new FormData()
formData.append("ward_id", form.ward_id)
console.log(formData)
