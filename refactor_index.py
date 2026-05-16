import re

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Base ImageKit URL for root images
base_url = "https://ik.imagekit.io/rx7rkge23/Portfolio%20Images%20Prayash/"

def replace_img(match):
    full_img_tag = match.group(0)
    src_val = match.group(1)
    
    if "assets/images/" in src_val and "assets/images/case1/" not in src_val:
        # Extract the relative path after "assets/images/"
        rel_path = src_val.split("assets/images/")[1]
        
        # We will use data-cdn-img attribute instead of src
        new_tag = re.sub(r'src=[\"\'\'][^\"\']+[\"\'\']', f'data-cdn-img="{rel_path}" src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 1 1\'%3E%3C/svg%3E"', full_img_tag)
        
        # Add cdn-image class
        if 'class="' in new_tag:
            new_tag = re.sub(r'class="([^"]+)"', r'class="\1 cdn-image"', new_tag)
        else:
            new_tag = new_tag.replace('<img', '<img class="cdn-image"')
            
        return new_tag
    return full_img_tag

new_content = re.sub(r'<img[^>]+src=[\"\'\']([^\"\']+)[\"\'\'][^>]*>', replace_img, content)

css = """
        /* ── CDN IMAGE COMPONENT ── */
        .cdn-image {
            opacity: 0;
            transform: scale(0.98);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out, filter 0.3s ease;
        }
        
        .cdn-image.loaded {
            opacity: 1;
            transform: scale(1);
        }
        
        .cdn-image.loaded:hover {
            filter: brightness(1.05);
        }
"""

js = """
    <!-- IMAGEKIT CDN SCRIPT -->
    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const baseUrl = "https://ik.imagekit.io/rx7rkge23/Portfolio%20Images%20Prayash/";
            
            const imageRegistry = [];
            
            const cdnImages = document.querySelectorAll('.cdn-image');
            cdnImages.forEach((img, index) => {
                const imgPath = img.getAttribute('data-cdn-img');
                if (imgPath) {
                    const fullUrl = baseUrl + imgPath;
                    imageRegistry.push({ element: img, url: fullUrl, id: index });
                }
            });
            
            const imgObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const registryItem = imageRegistry.find(item => item.element === img);
                        
                        if (registryItem) {
                            const tempImg = new Image();
                            tempImg.onload = () => {
                                img.src = registryItem.url;
                                img.classList.add('loaded');
                            };
                            tempImg.src = registryItem.url;
                        }
                        
                        observer.unobserve(img);
                    }
                });
            }, { rootMargin: '100px' });
            
            imageRegistry.forEach(item => {
                imgObserver.observe(item.element);
            });
        });
    </script>
"""

new_content = new_content.replace("</style>", css + "</style>")
new_content = new_content.replace("</body>", js + "\n</body>")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
