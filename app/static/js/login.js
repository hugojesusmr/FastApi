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
    emailGroup.style.display = isLogin ? 'none' : 'block';
    const emailInput = emailGroup.querySelector('input[name="email"]');
    if (isLogin) {
        emailInput.removeAttribute('required');
    } else {
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
    const data = Object.fromEntries(formData);

    try {
        const endpoint = isLogin ? '/auth/login' : '/auth/register';
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

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
