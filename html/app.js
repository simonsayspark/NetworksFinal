// Fetch files from the API endpoint proxied by Nginx
async function fetchFiles() {
    try {
      const response = await fetch('/api/files'); // Updated API endpoint
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const files = await response.json();
      displayFiles(files);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  }
  
  // Dynamically display the files on the page
  function displayFiles(files) {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = ''; // Clear any existing content
    files.forEach(file => {
      const listItem = document.createElement('li');
      const link = document.createElement('a');
      link.href = `/files/${file.filename}`; // Link to the static files folder
      link.textContent = file.filename;
      link.target = '_blank'; // Open in a new tab
      listItem.appendChild(link);
      fileList.appendChild(listItem);
    });
  }
  
  // Call fetchFiles when the page loads
  document.addEventListener('DOMContentLoaded', fetchFiles);
  