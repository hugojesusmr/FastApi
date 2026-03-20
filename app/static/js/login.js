const form = document.getElementById('loginForm');
const toggleBtn = document.getElementById('toggleBtn');
const submitBtn = document.getElementById('submitBtn');
const errorMsg = document.getElementById('errorMessage');
const title = document.getElementById('title');
const emailGroup = document.getElementById('emailGroup');
let isLogin = true;

toggleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    isLogin = !isLogin;
    title.textContent = isLogin ? 'Iniciar Sesión' : 'Registrarse';
    submitBtn.textContent = isLogin ? 'Iniciar Sesión' : 'Registrarse';
    toggleBtn.textContent = isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión';
    
    const emailInput = emailGroup.querySelector('input[name="email"]');
    if (isLogin) {
        emailGroup.style.display = 'none';
        emailInput.removeAttribute('required');
    } else {
        emailGroup.style.display = 'block';
        emailInput.setAttribute('required', 'required');
    }
    errorMsg.style.display = 'none';
    form.reset();
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Procesando...';
    errorMsg.style.display = 'none';

    const formData = new FormData(form);
    let data = Object.fromEntries(formData);
    
    // Filtrar datos según el modo
    if (isLogin) {
        data = { username: data.username, password: data.password };
    } else {
        data = { email: data.email, username: data.username, password: data.password };
    }

    try {
        const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
        console.log('Enviando datos:', data);
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log('Respuesta del servidor:', result);

        if (!response.ok) {
            throw new Error(result.detail || 'Error en la operación');
        }

        if (isLogin) {
            localStorage.setItem('access_token', result.access_token);
            localStorage.setItem('username', data.username);
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 500);
        } else {
            isLogin = true;
            title.textContent = 'Iniciar Sesión';
            submitBtn.textContent = 'Iniciar Sesión';
            toggleBtn.textContent = '¿No tienes cuenta? Regístrate';
            emailGroup.style.display = 'none';
            form.reset();
            errorMsg.textContent = 'Registro exitoso. Ahora puedes iniciar sesión.';
            errorMsg.classList.add('success');
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.textContent = err.message;
        errorMsg.classList.remove('success');
        errorMsg.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = isLogin ? 'Iniciar Sesión' : 'Registrarse';
    }
});
