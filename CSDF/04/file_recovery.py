"""To develop a Python-based computer forensics application that scans storage devices 
or disk images to identify recoverable deleted files and detect lost or deleted partitions 
while preserving the integrity of digital evidence."""

import os
import hashlib

# Calculate SHA-256 hash to identify the original evidence
def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()


# Recover files using common file signatures
def recover_files(data, output_folder):
    signatures = [
        ("JPG", b"\xff\xd8\xff", b"\xff\xd9"),
        ("PNG", b"\x89PNG\r\n\x1a\n", b"IEND\xaeB`\x82"),
        ("PDF", b"%PDF-", b"%%EOF")
    ]

    os.makedirs(output_folder, exist_ok=True)
    recovered = 0

    for extension, start_sig, end_sig in signatures:
        position = 0

        while True:
            start = data.find(start_sig, position)
            if start == -1:
                break

            end = data.find(end_sig, start + len(start_sig))

            if end == -1:
                position = start + len(start_sig)
                continue

            end += len(end_sig)
            file_data = data[start:end]

            if len(file_data) > len(start_sig) + len(end_sig):
                recovered += 1
                filename = os.path.join(
                    output_folder, f"recovered_{recovered}.{extension.lower()}"
                )

                with open(filename, "wb") as output:
                    output.write(file_data)

                print(f"Recovered: {filename}")

            position = end

    if recovered == 0:
        print("No recoverable JPG, PNG, or PDF files found.")


# Examine partition information in a disk image
def scan_partitions(data):
    print("\n===== PARTITION ANALYSIS =====")

    if len(data) < 512:
        print("Image is too small to contain a standard MBR.")
        return

    # MBR signature is stored at bytes 510 and 511
    if data[510:512] == b"\x55\xaa":
        print("MBR signature found.")

        found = False

        # MBR partition entries occupy bytes 446 to 509
        for i in range(4):
            offset = 446 + i * 16
            entry = data[offset:offset + 16]
            partition_type = entry[4]
            start_sector = int.from_bytes(entry[8:12], "little")
            sectors = int.from_bytes(entry[12:16], "little")

            if partition_type != 0 and sectors > 0:
                found = True
                print(
                    f"Partition {i + 1}: Type={partition_type:#04x}, "
                    f"Start sector={start_sector}, Size={sectors} sectors"
                )

        if not found:
            print("No active MBR partition entries found.")
    else:
        print("Valid MBR signature not found.")

    # Check for primary or backup GPT headers
    primary_gpt = data[512:520] == b"EFI PART"
    backup_gpt = False

    # GPT backup header is normally at the final logical sector
    for sector_size in (512, 4096):
        if len(data) >= sector_size:
            if data[-sector_size:-sector_size + 8] == b"EFI PART":
                backup_gpt = True

    print("Primary GPT header:", "Found" if primary_gpt else "Not found")
    print("Backup GPT header:", "Found" if backup_gpt else "Not found")

    if backup_gpt and not primary_gpt:
        print("Possible damaged or missing primary GPT metadata.")
    elif not primary_gpt and not backup_gpt:
        print("GPT partition recovery cannot be confirmed from these checks.")


def main():
    image_path = input("Enter disk image path: ").strip().strip('"')

    try:
        with open(image_path, "rb") as file:
            data = file.read()
    except OSError as error:
        print("Unable to read disk image:", error)
        return

    print("\n===== DIGITAL FORENSICS REPORT =====")
    print("Image size:", len(data), "bytes")
    print("SHA-256:", calculate_hash(data))

    scan_partitions(data)

    print("\n===== DELETED FILE RECOVERY =====")
    recover_files(data, "recovered_files")

    print("\nScan completed. Original image was not modified.")


if __name__ == "__main__":
    main()
