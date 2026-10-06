document.addEventListener("DOMContentLoaded", () => {
    const reader = document.getElementById("reader");
    const form = document.getElementById("scan-form");
    const input = document.getElementById("barcode-input");

    if (!reader || !form || !input) {
        return;
    }

    let scanCompleted = false;

    const scanner = new Html5QrcodeScanner(
        "reader",
        {
            fps: 10,
            qrbox: {
                width: 280,
                height: 160,
            },
            rememberLastUsedCamera: true,
        },
        false
    );

    const onScanSuccess = async (decodedText) => {
        if (scanCompleted) {
            return;
        }

        scanCompleted = true;

        input.value = decodedText.trim();

        try {
            await scanner.clear();
        } catch (error) {
            console.error(error);
        }

        form.submit();
    };

    const onScanFailure = () => {
        // Der skal ikke vises en fejl for hvert kamera-frame,
        // hvor der endnu ikke er fundet en stregkode.
    };

    scanner.render(
        onScanSuccess,
        onScanFailure
    );
});