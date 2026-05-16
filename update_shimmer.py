import re

def update_file(html_file, is_case1=True):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    base_url = 'https://ik.imagekit.io/rx7rkge23/Portfolio%20Images%20Prayash/case1/' if is_case1 else 'https://ik.imagekit.io/rx7rkge23/Portfolio%20Images%20Prayash/'

    def replace_to_direct(match):
        tag = match.group(0)
        data_img = match.group(1)
        
        # Remove the data:image/svg placeholder
        tag = re.sub(r'\s*src=[\"\'\']data:image/svg\+xml[^\"\']+[\"\'\']', '', tag)
        
        # Replace data-cdn-img with actual src
        tag = tag.replace(f'data-cdn-img="{data_img}"', f'src="{base_url}{data_img}"')
        
        return tag

    new_content = re.sub(r'<img[^>]+data-cdn-img=[\"\'\']([^\"\']+)[\"\'\'][^>]*>', replace_to_direct, content)

    css = """
        /* ── CDN IMAGE COMPONENT ── */
        .cdn-image {
            background: #f6f7f8;
            background: linear-gradient(to right, #eeeeee 8%, #dddddd 18%, #eeeeee 33%);
            background-size: 800px 104px;
            animation: shimmer 1.5s linear infinite forwards;
            color: transparent;
        }
        
        .cdn-image.loaded {
            background: transparent;
            animation: none;
        }
        
        @keyframes shimmer {
            0% { background-position: -468px 0; }
            100% { background-position: 468px 0; }
        }
"""
    # Replace the old CSS
    old_css_pattern = r'/\*\s*── CDN IMAGE COMPONENT ──\s*\*/.*?\.cdn-image\.loaded:hover\s*{[^}]*}'
    new_content = re.sub(old_css_pattern, css.strip(), new_content, flags=re.DOTALL)
    
    # Replace the old JS
    old_js_pattern = r'<!-- IMAGEKIT CDN SCRIPT -->.*?</script>'
    
    js = """<!-- IMAGEKIT CDN SCRIPT -->
    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const cdnImages = document.querySelectorAll('.cdn-image');
            cdnImages.forEach(img => {
                if (img.complete) {
                    img.classList.add('loaded');
                } else {
                    img.addEventListener('load', () => {
                        img.classList.add('loaded');
                    });
                }
            });
        });
    </script>"""
    
    new_content = re.sub(old_js_pattern, js, new_content, flags=re.DOTALL)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

update_file('case1.html', is_case1=True)
update_file('index.html', is_case1=False)
