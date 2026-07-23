import re

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "r") as f:
    content = f.read()

# Add import API_URL
if "import { API_URL" not in content:
    content = content.replace('import Link from "next/link";', 'import Link from "next/link";\nimport { API_URL } from "@/constants/endpoints";')

# Inject getFinalImageUri globally
if "const getFinalImageUri" not in content:
    helper = """
const getFinalImageUri = (img: string) => {
  let finalUri = img;
  if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
    const base = API_URL ? API_URL.replace(/\\/api\\/v1\\/?$/, '') : '';
    let path = img.startsWith('/') ? img : '/' + img;
    if (!path.startsWith('/uploads/')) {
      path = '/uploads' + path;
    }
    finalUri = `${base}${path}`;
  }
  return finalUri;
};
"""
    content = content.replace("export default function ComplaintDetailsPage() {", helper + "\nexport default function ComplaintDetailsPage() {")

# Extract the complaintImages
# Replace the old rendering block
old_render = """          {complaint.image_urls && complaint.image_urls.length > 0 && (
            <div className="mt-8 pt-6 border-t border-border/50">
              <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4">Attached Images</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {complaint.image_urls.map((url: string, index: number) => (
                  <div 
                    key={index} 
                    className="relative aspect-square rounded-2xl overflow-hidden border border-border shadow-sm cursor-pointer group"
                    onClick={() => setSelectedImagePreview(url)}
                  >
                    <img src={url} alt={`Complaint ${index+1}`} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  </div>
                ))}
              </div>
            </div>
          )}"""

new_render = """          {(() => {
            let complaintImages: string[] = [];
            if (Array.isArray(complaint.images) && complaint.images.length > 0) {
              complaintImages = complaint.images;
            } else if (Array.isArray(complaint.image_urls) && complaint.image_urls.length > 0) {
              complaintImages = complaint.image_urls;
            } else if (Array.isArray(complaint.proof_images) && complaint.proof_images.length > 0) {
              complaintImages = complaint.proof_images;
            }

            if (complaintImages.length > 0) {
              return (
                <div className="mt-8 pt-6 border-t border-border/50">
                  <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4">Attached Photos</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {complaintImages.map((url: string, index: number) => {
                      const finalUrl = getFinalImageUri(url);
                      console.log(`[Web] Rendering Image: ${url} -> ${finalUrl}`);
                      return (
                        <div 
                          key={index} 
                          className="relative aspect-square rounded-2xl overflow-hidden border border-border shadow-sm cursor-pointer group"
                          onClick={() => setSelectedImagePreview(finalUrl)}
                        >
                          <img src={finalUrl} alt={`Complaint ${index+1}`} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            }
            return null;
          })()}"""

content = content.replace(old_render, new_render)

# Add useEffect for logs
log_effect = """
  useEffect(() => {
    if (complaint) {
      console.log("--- WEB COMPLAINT RESPONSE ---");
      console.log("Complete complaint object:", complaint);
      console.log("complaint.images:", complaint.images);
      console.log("complaint.image_urls:", complaint.image_urls);
      console.log("complaint.proof_images:", complaint.proof_images);
    }
  }, [complaint]);
"""

if "console.log(\"--- WEB COMPLAINT RESPONSE ---\");" not in content:
    content = content.replace("  const typeMeta = TYPE_META[complaint.complaint_type] || TYPE_META.OTHER;", log_effect + "\n  const typeMeta = TYPE_META[complaint.complaint_type] || TYPE_META.OTHER;")

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "w") as f:
    f.write(content)

print("Web rendering fixed.")
