const tableBody = document.getElementById('tableBody');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');
const uploadBtn = document.getElementById('uploadBtn');
const activeFiltersDiv = document.getElementById('activeFilters');

let currentPage = 1;
const itemsPerPage = 15;
let allRegions = [];

const filters = {
    id: '',
    siteCode: '',
    location: '',
    service: '',
    city: '',
    state: '',
    network: '',
    region: '',
    coordinator: '',
    engineer: '',
    km: '',
    engineering: '',
    kmz: ''
};

const filterLabels = {
    id: 'ID',
    siteCode: 'Site Code',
    location: 'Ubicación',
    service: 'Service PANDA',
    city: 'Ciudad',
    state: 'Estado',
    network: 'Tipo de Red',
    region: 'Región',
    coordinator: 'Coordinador',
    engineer: 'Ingeniero',
    km: 'KM',
    engineering: 'Ingeniería',
    kmz: 'KMZ'
};

async function loadRegions() {
    try {
        const queryParams = new URLSearchParams();
        queryParams.append('skip', 0);
        queryParams.append('limit', 1000);
        
        Object.keys(filters).forEach(key => {
            if (filters[key] && filters[key].trim()) {
                if (key === 'siteCode') {
                    queryParams.append('site_code', filters[key]);
                } else if (key === 'location') {
                    queryParams.append('location_name', filters[key]);
                } else if (key === 'service') {
                    queryParams.append('service_panda', filters[key]);
                } else if (key === 'network') {
                    queryParams.append('tipo_de_red', filters[key]);
                } else if (key === 'coordinator') {
                    queryParams.append('coordinador', filters[key]);
                } else if (key === 'engineer') {
                    queryParams.append('ingeniero', filters[key]);
                } else if (key === 'engineering') {
                    queryParams.append('ingenieria', filters[key]);
                } else {
                    queryParams.append(key, filters[key]);
                }
            }
        });

        const response = await fetch(`/regions/?${queryParams.toString()}`);
        const data = await response.json();
        allRegions = data;
        currentPage = 1;
        renderTable();
    } catch (err) {
        tableBody.innerHTML = `<tr class="empty-row"><td colspan="15">Error al cargar datos: ${err.message}</td></tr>`;
    }
}

function renderTable() {
    if (allRegions.length === 0) {
        tableBody.innerHTML = '<tr class="empty-row"><td colspan="15">No hay datos que coincidan con los filtros</td></tr>';
        updatePagination();
        return;
    }

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = allRegions.slice(start, end);

    let html = '';
    pageData.forEach(region => {
        html += `<tr data-id="${region.id}"><td>${region.id || '-'}</td><td>${region.site_code || '-'}</td><td>${region.location_name || '-'}</td><td>${region.service_panda || '-'}</td><td>${region.city || '-'}</td><td>${region.state || '-'}</td><td>${region.tipo_de_red || '-'}</td><td>${region.region || '-'}</td><td>${region.coordinador || '-'}</td><td>${region.ingeniero || '-'}</td><td>${region.km || '-'}</td><td>${region.ingenieria || '-'}</td><td>${region.kmz || '-'}</td><td style="text-align: center; position: relative;"><button class="action-btn" onclick="toggleMenu(event, ${region.id})" style="background: none; border: none; cursor: pointer; font-size: 18px; padding: 0; color: #00d4ff;">⋮</button><div id="menu-${region.id}" class="action-menu" style="display: none; position: absolute; top: 100%; right: 0; background: white; border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); z-index: 1000; min-width: 120px;" onclick="event.stopPropagation();"><button onclick="viewRegion(${region.id}); event.stopPropagation();" style="display: block; width: 100%; padding: 10px 12px; border: none; background: none; text-align: left; cursor: pointer; font-size: 12px; color: #2d3748;">👁️ Ver</button><button onclick="editRegion(${region.id}); event.stopPropagation();" style="display: block; width: 100%; padding: 10px 12px; border: none; background: none; text-align: left; cursor: pointer; font-size: 12px; color: #2d3748;">✏️ Editar</button><button onclick="deleteRegion(${region.id}); event.stopPropagation();" style="display: block; width: 100%; padding: 10px 12px; border: none; background: none; text-align: left; cursor: pointer; font-size: 12px; color: #e53e3e;">🗑️ Actualizar</button></div></td></tr>`;
    });
    tableBody.innerHTML = html;
    updatePagination();
}

function updatePagination() {
    const totalPages = Math.ceil(allRegions.length / itemsPerPage);
    pageInfo.textContent = `Página ${currentPage} de ${totalPages || 1}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages || totalPages === 0;
}

function updateActiveFilters() {
    activeFiltersDiv.innerHTML = '';
    
    Object.keys(filters).forEach(key => {
        if (filters[key] && filters[key].trim()) {
            const filterTag = document.createElement('div');
            filterTag.style.cssText = 'display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: linear-gradient(135deg, #00d4ff 0%, #00b8ff 100%); border-radius: 20px; color: white; font-size: 12px; font-weight: 600;';
            
            filterTag.innerHTML = `
                ${filterLabels[key]}
                <button onclick="clearFilter('${key}')" style="background: none; border: none; color: white; cursor: pointer; font-size: 16px; padding: 0;">×</button>
            `;
            activeFiltersDiv.appendChild(filterTag);
        }
    });
}

function clearFilter(key) {
    filters[key] = '';
    const inputId = {
        id: 'filterId',
        siteCode: 'filterSiteCode',
        location: 'filterLocation',
        service: 'filterService',
        city: 'filterCity',
        state: 'filterState',
        network: 'filterNetwork',
        region: 'filterRegion',
        coordinator: 'filterCoordinator',
        engineer: 'filterEngineer',
        km: 'filterKM',
        engineering: 'filterEngineering',
        kmz: 'filterKMZ'
    }[key];
    
    const element = document.getElementById(inputId);
    if (element) element.value = '';
    updateActiveFilters();
    loadRegions();
}

function toggleMenu(event, regionId) {
    event.stopPropagation();
    const menu = document.getElementById(`menu-${regionId}`);
    const isOpen = menu.style.display === 'block';
    document.querySelectorAll('[id^="menu-"]').forEach(m => m.style.display = 'none');
    if (!isOpen) menu.style.display = 'block';
}

function viewRegion(regionId) {
    alert(`Ver región ${regionId}`);
}

function editRegion(regionId) {
    alert(`Editar región ${regionId}`);
}

function deleteRegion(regionId) {
    if (confirm(`¿Actualizar región ${regionId}?`)) {
        alert(`Región ${regionId} actualizada`);
    }
}

document.addEventListener('click', (event) => {
    if (!event.target.closest('[id^="menu-"]') && !event.target.closest('button[onclick*="toggleMenu"]')) {
        document.querySelectorAll('[id^="menu-"]').forEach(m => m.style.display = 'none');
    }
});

prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
    }
});

nextBtn.addEventListener('click', () => {
    const totalPages = Math.ceil(allRegions.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
    }
});

const filterInputs = {
    filterId: 'id',
    filterSiteCode: 'siteCode',
    filterLocation: 'location',
    filterService: 'service',
    filterCity: 'city',
    filterState: 'state',
    filterNetwork: 'network',
    filterRegion: 'region',
    filterCoordinator: 'coordinator',
    filterEngineer: 'engineer',
    filterKM: 'km',
    filterEngineering: 'engineering',
    filterKMZ: 'kmz'
};

Object.keys(filterInputs).forEach(inputId => {
    const element = document.getElementById(inputId);
    if (element) {
        element.addEventListener('input', (e) => {
            filters[filterInputs[inputId]] = e.target.value;
            updateActiveFilters();
            loadRegions();
        });
    }
});

loadRegions();

if (uploadBtn) {
    uploadBtn.addEventListener('click', () => {
        setTimeout(() => {
            loadRegions();
        }, 1000);
    });
}
