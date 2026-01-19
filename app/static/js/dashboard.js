Dropzone.autoDiscover = false;

const dropzone = new Dropzone("#uploadForm", {
    maxFilesize: 100,
    acceptedFiles: ".xlsx,.xls,.csv,.json",
    addRemoveLinks: false,
    autoProcessQueue: false
});

const uploadFilesBtn = document.getElementById('uploadFilesBtn');
const uploadStatus = document.getElementById('uploadStatus');
const fileList = document.getElementById('fileList');
const filesContainer = document.getElementById('filesContainer');

let selectedFiles = [];

dropzone.on('addedfile', (file) => {
    selectedFiles.push(file);
    renderFileList();
});

dropzone.on('removedfile', (file) => {
    selectedFiles = selectedFiles.filter(f => f !== file);
    renderFileList();
});

function renderFileList() {
    if (selectedFiles.length === 0) {
        fileList.style.display = 'none';
        filesContainer.innerHTML = '';
        return;
    }

    fileList.style.display = 'block';
    filesContainer.innerHTML = selectedFiles.map((file, index) => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: rgba(0, 212, 255, 0.05); border-radius: 8px; border: 1px solid rgba(0, 212, 255, 0.2);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">📄</span>
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: #2d3748;">${file.name}</div>
                    <div style="font-size: 12px; color: #a0aec0;">${(file.size / 1024).toFixed(2)} KB</div>
                </div>
            </div>
            <button type="button" onclick="removeFile(${index})" style="padding: 6px 12px; background: rgba(220, 38, 38, 0.08); color: #dc2626; border: 1px solid rgba(220, 38, 38, 0.3); border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                Eliminar
            </button>
        </div>
    `).join('');
}

function removeFile(index) {
    const file = selectedFiles[index];
    dropzone.removeFile(file);
}


uploadFilesBtn.addEventListener('click', async () => {
    if (selectedFiles.length === 0) {
        showUploadStatus('Selecciona un archivo', 'error');
        return;
    }

    const file = selectedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    uploadFilesBtn.disabled = true;
    uploadFilesBtn.innerHTML = '<span class="cloud-loading">☁️</span> Subiendo...';
    showUploadStatus('Cargando...', 'loading');

    try {
        const response = await fetch('http://localhost:8000/regions/upload-excel', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error al cargar el archivo');
        }

        showUploadStatus(`✓ ${result.message}`, 'success');
        dropzone.removeAllFiles();
        loadRegionsTable();
    } catch (err) {
        showUploadStatus(`✗ ${err.message}`, 'error');
    } finally {
        uploadFilesBtn.disabled = false;
        uploadFilesBtn.innerHTML = 'Subir';
    }
});

function showUploadStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `upload-status ${type}`;
    if (type === 'success') {
        uploadStatus.style.color = '#16a34a';
    } else if (type === 'error') {
        uploadStatus.style.color = '#dc2626';
    } else {
        uploadStatus.style.color = '#00d4ff';
    }
}

window.addEventListener('load', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
    }
    loadUserInfo();
});

function loadUserInfo() {
    const username = localStorage.getItem('username') || 'Usuario';
    document.getElementById('userName').textContent = username;
    document.getElementById('userAvatar').textContent = username.charAt(0).toUpperCase();
}

function switchTab(tab) {
    document.querySelectorAll('[id$="-tab"]').forEach(el => {
        el.style.display = 'none';
    });
    document.getElementById(tab + '-tab').style.display = 'block';

    document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active');
    });
    event.target.closest('.nav-link').classList.add('active');
    
    if (tab === 'regions') {
        loadRegionsTable();
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('expanded');
}

async function loadRegionsTable() {
    // Esta función ya no se usa, regions.js maneja la tabla
    return;
}
