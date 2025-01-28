async function downloadMusic() {
  const videoUrl = document.getElementById("videoUrl").value;
  const format = document.getElementById("format").value;
  const quality = document.getElementById("quality").value;
  const status = document.getElementById("status");

  if (!videoUrl) {
    status.textContent = "Please enter a valid YouTube video URL";
    return;
  }

  status.textContent = "Processing your request...";

  try {
    const response = await fetch("/api/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ videoUrl, format, quality }),
    });

    if (response.ok) {
      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `download.${format}`;
      link.click();
      status.textContent = "Download successful!";
    } else {
      const error = await response.text();
      status.textContent = `Error: ${error}`;
    }
  } catch (error) {
    status.textContent = "An error occurred. Please try again later.";
  }
}
