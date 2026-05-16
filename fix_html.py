def fix_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed_content = content.replace("http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E\"", "")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

fix_file('case1.html')
fix_file('index.html')
