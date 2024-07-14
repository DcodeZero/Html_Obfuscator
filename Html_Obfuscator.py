import base64
import os
import sys
import argparse

def encode_html(html_content):
    return base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

def decode_html(encoded_content):
    return base64.b64decode(encoded_content).decode('utf-8')

def generate_obfuscated_html(encoded_content):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Obfuscated HTML</title>
    <script type="text/javascript">
        function decodeHTML(encoded) {{
            var decoded = atob(encoded);
            document.write(decoded);
        }}
    </script>
</head>
<body onload="decodeHTML('{encoded_content}')">
</body>
</html>
"""

def extract_encoded_content(obfuscated_html_content):
    start_tag = "decodeHTML('"
    end_tag = "')"
    start_index = obfuscated_html_content.find(start_tag) + len(start_tag)
    end_index = obfuscated_html_content.find(end_tag)
    return obfuscated_html_content[start_index:end_index]

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def obfuscate_html_file(input_file_path, output_file_path):
    html_content = read_file(input_file_path)
    encoded_content = encode_html(html_content)
    obfuscated_html = generate_obfuscated_html(encoded_content)
    write_file(output_file_path, obfuscated_html)
    print(f"Obfuscated HTML has been saved to {output_file_path}")

def deobfuscate_html_file(input_file_path, output_file_path):
    obfuscated_html_content = read_file(input_file_path)
    encoded_content = extract_encoded_content(obfuscated_html_content)
    decoded_html = decode_html(encoded_content)
    write_file(output_file_path, decoded_html)
    print(f"Deobfuscated HTML has been saved to {output_file_path}")

def process_directory(directory_path, operation, output_directory):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".html"):
            file_path = os.path.join(directory_path, file_name)
            output_file_path = os.path.join(output_directory, f"{operation}_{file_name}")
            if operation == "obfuscated":
                obfuscate_html_file(file_path, output_file_path)
            elif operation == "deobfuscated":
                deobfuscate_html_file(file_path, output_file_path)

def main():
    parser = argparse.ArgumentParser(description='Obfuscate or Deobfuscate HTML files.')
    parser.add_argument('-oF', '--obfuscate', action='store_true', help='Obfuscate a single HTML file')
    parser.add_argument('-oD', '--deobfuscate', action='store_true', help='Deobfuscate a single HTML file')
    parser.add_argument('-p', '--path', type=str, help='Path to the HTML file')
    parser.add_argument('-P', '--directory', type=str, help='Path to the directory containing HTML files')
    parser.add_argument('-o', '--output', type=str, help='Output path for the single file')
    parser.add_argument('-O', '--output_directory', type=str, help='Output directory for the processed files')
    
    args = parser.parse_args()

    if args.obfuscate and args.path and args.output:
        obfuscate_html_file(args.path, args.output)
    elif args.deobfuscate and args.path and args.output:
        deobfuscate_html_file(args.path, args.output)
    elif args.obfuscate and args.directory and args.output_directory:
        process_directory(args.directory, "obfuscated", args.output_directory)
    elif args.deobfuscate and args.directory and args.output_directory:
        process_directory(args.directory, "deobfuscated", args.output_directory)
    else:
        print("Usage: python html_obfuscator.py -oF <obfuscate> -oD <deobfuscate> -p <path for single file> -P <path_to_directory> -o <output_single_file> -O <output_multiple_files_to_directory>")
        sys.exit(1)

if __name__ == "__main__":
    main()
