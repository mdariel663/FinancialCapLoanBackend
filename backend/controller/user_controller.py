# users/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import json
from models.models import User 

@csrf_exempt
@require_POST
def create_user(request):
    """
    Registra un nuevo usuario en la base de datos.

    Espera un cuerpo JSON con los campos 'username', 'email' y 'password'.
    Retorna un mensaje de éxito o un error en caso de que los campos falten
    o se produzca un error en la base de datos.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Se esperaba un cuerpo JSON'}, status=400)
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return JsonResponse({'error': 'Faltan campos obligatorios: username, email y password'}, status=400)

    # Verifica si el correo electrónico ya existe
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'El correo electrónico ya está en uso.'}, status=400)

    # Crea el nuevo usuario y encripta la contraseña
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Usa set_password para encriptar la contraseña
    try:
        new_user.save()
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Usuario creado correctamente'}, status=201)

@csrf_exempt
@require_POST
def login(request):
    """
    Inicia sesión para un usuario existente.

    Espera un cuerpo JSON con los campos 'username' y 'password'.
    Verifica las credenciales y retorna un mensaje de éxito o un error
    en caso de que las credenciales sean incorrectas.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Se esperaba un cuerpo JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Faltan campos obligatorios: username y password'}, status=400)

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
        else:
            return JsonResponse({'message': 'Credenciales incorrectas'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Credenciales incorrectas'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def get_users(request):
    """
    Obtiene la lista de todos los usuarios registrados.

    Returns:
        JSON: Lista de usuarios con su ID y nombre de usuario.
    """
    users = User.objects.all()  # Obtener todos los usuarios de la base de datos
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse(user_list, safe=False)

@csrf_exempt
@require_POST
def register_user(request):
    """
    Registra un nuevo usuario con un rol específico.

    Espera un cuerpo JSON con los campos 'username', 'password' y 'role'.
    Retorna un mensaje de éxito o un error en caso de que los campos falten
    o se produzca un error en la base de datos.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Se esperaba un cuerpo JSON'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return JsonResponse({'error': 'Faltan campos obligatorios: username, password y role'}, status=400)

    # Verifica si el nombre de usuario ya existe
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'El nombre de usuario ya está en uso.'}, status=400)

    # Crea el nuevo usuario y encripta la contraseña
    new_user = User(username=username)
    new_user.set_password(password)
    new_user.role = role  # Asumiendo que has agregado un campo 'role' al modelo User
    try:
        new_user.save()
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Usuario registrado correctamente'}, status=201)