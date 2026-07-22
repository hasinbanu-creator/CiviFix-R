import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

# 1. Add ImagePicker import
if "import * as ImagePicker from 'expo-image-picker'" not in content:
    content = content.replace(
        'import { SPACING } from "../../constants/theme";',
        'import { SPACING } from "../../constants/theme";\nimport * as ImagePicker from "expo-image-picker";'
    )

# 2. Add state for selectedProofImages
state_old = """  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [reopenReason, setReopenReason] = useState("");
  const [submitting, setSubmitting] = useState(false);"""

state_new = """  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [reopenReason, setReopenReason] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [selectedProofImages, setSelectedProofImages] = useState([]);
  const [resolveNote, setResolveNote] = useState("");"""

content = content.replace(state_old, state_new)

# 3. Handle picking images
pick_logic = """  const pickProofImages = async () => {
    if (selectedProofImages.length >= 5) {
      alert("You can attach up to 5 proof images.");
      return;
    }
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (permission.status !== "granted") {
      alert("Permission to access gallery is required!");
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsMultipleSelection: true,
      selectionLimit: 5 - selectedProofImages.length,
      quality: 0.8,
    });
    if (!result.canceled && result.assets) {
      const newImages = result.assets.map((asset) => ({
        uri: asset.uri,
        name: asset.fileName || `proof-${Date.now()}.jpg`,
        type: asset.type || "image/jpeg",
      }));
      setSelectedProofImages([...selectedProofImages, ...newImages].slice(0, 5));
    }
  };

  const takeProofPhoto = async () => {
    if (selectedProofImages.length >= 5) {
      alert("You can attach up to 5 proof images.");
      return;
    }
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (permission.status !== "granted") {
      alert("Permission to access camera is required!");
      return;
    }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled && result.assets) {
      const asset = result.assets[0];
      const newImage = {
        uri: asset.uri,
        name: asset.fileName || `proof-cam-${Date.now()}.jpg`,
        type: asset.type || "image/jpeg",
      };
      setSelectedProofImages([...selectedProofImages, newImage].slice(0, 5));
    }
  };"""

content = content.replace("  const handleResolve = async () => {", pick_logic + "\n\n  const handleResolve = async () => {")

# 4. Update handleResolve
handleResolve_old = """  const handleResolve = async () => {
    try {
      setSubmitting(true);
      const proofImages = Array.isArray(complaint?.image_urls) && complaint.image_urls.length > 0
        ? complaint.image_urls
        : Array.isArray(complaint?.proof_images) && complaint.proof_images.length > 0
          ? complaint.proof_images
          : [];

      if (proofImages.length === 0) {
        alert("Please attach at least one proof image before resolving this complaint.");
        return;
      }

      await authService.inspectorResolveComplaint(complaintId, {
        proof_images: proofImages,
        note: "Resolved by inspector after verification",
      });
      alert("Complaint resolved!");
      const data = await authService.getComplaint(complaintId);
      setComplaint(data);
    } catch (err) {
      alert(getErrorMessage(err, "Failed to resolve complaint"));
    } finally {
      setSubmitting(false);
    }
  };"""

handleResolve_new = """  const handleResolve = async () => {
    try {
      setSubmitting(true);
      if (selectedProofImages.length === 0) {
        alert("Please attach at least one proof image.");
        setSubmitting(false);
        return;
      }

      const formData = new FormData();
      if (resolveNote.trim()) {
        formData.append("note", resolveNote.trim());
      }
      
      selectedProofImages.forEach((img, index) => {
        formData.append("images", img);
      });

      await authService.inspectorResolveComplaint(complaintId, formData);
      alert("Complaint resolved successfully!");
      const data = await authService.getComplaint(complaintId);
      setComplaint(data);
    } catch (err) {
      alert(getErrorMessage(err, "Failed to resolve complaint"));
    } finally {
      setSubmitting(false);
    }
  };"""

content = content.replace(handleResolve_old, handleResolve_new)

# 5. Update Inspector Actions UI for In Progress
ui_old = """              {["in_progress", "working"].includes(complaint.status?.toLowerCase()) && (
                <TouchableOpacity style={[styles.actionBtn, { backgroundColor: "#059669" }]} onPress={handleResolve} disabled={submitting}>
                  {submitting ? <ActivityIndicator size="small" color="#fff" /> : <Text style={styles.actionBtnText}>Resolve</Text>}
                </TouchableOpacity>
              )}"""

ui_new = """              {["in_progress", "working"].includes(complaint.status?.toLowerCase()) && (
                <View style={{ marginTop: 10 }}>
                  <Text style={{ fontSize: 14, fontWeight: '700', marginBottom: 10, color: '#333' }}>Attach Proof (Required)</Text>
                  
                  <View style={{ flexDirection: "row", gap: 10, marginBottom: 15 }}>
                    <TouchableOpacity style={[styles.actionBtn, { flex: 1, backgroundColor: '#0284c7' }]} onPress={takeProofPhoto}>
                      <Text style={styles.actionBtnText}>Camera</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={[styles.actionBtn, { flex: 1, backgroundColor: '#4f46e5' }]} onPress={pickProofImages}>
                      <Text style={styles.actionBtnText}>Gallery</Text>
                    </TouchableOpacity>
                  </View>

                  {selectedProofImages.length > 0 && (
                    <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: 15 }}>
                      {selectedProofImages.map((img, idx) => (
                        <View key={`proof-${idx}`} style={{ position: 'relative', marginRight: 10 }}>
                          <Image source={{ uri: img.uri }} style={{ width: 80, height: 80, borderRadius: 8 }} />
                          <TouchableOpacity
                            style={{ position: 'absolute', top: -5, right: -5, backgroundColor: 'red', borderRadius: 12, width: 24, height: 24, alignItems: 'center', justifyContent: 'center' }}
                            onPress={() => setSelectedProofImages(prev => prev.filter((_, i) => i !== idx))}
                          >
                            <Icon name="close" size={16} color="white" />
                          </TouchableOpacity>
                        </View>
                      ))}
                    </ScrollView>
                  )}

                  <TextInput
                    style={styles.textInput}
                    placeholder="Resolution notes (optional)"
                    value={resolveNote}
                    onChangeText={setResolveNote}
                    multiline
                  />

                  <TouchableOpacity 
                    style={[styles.actionBtn, { backgroundColor: selectedProofImages.length > 0 ? "#059669" : "#a1a1aa", marginTop: 10 }]} 
                    onPress={handleResolve} 
                    disabled={submitting || selectedProofImages.length === 0}
                  >
                    {submitting ? <ActivityIndicator size="small" color="#fff" /> : <Text style={styles.actionBtnText}>Submit & Resolve</Text>}
                  </TouchableOpacity>
                </View>
              )}"""

content = content.replace(ui_old, ui_new)

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

