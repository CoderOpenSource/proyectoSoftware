from django.http import JsonResponse
from django.conf import settings
import logging
from opentok import OpenTok, MediaModes, Roles, ArchiveModes

logger = logging.getLogger(__name__)

def generar_sesion_vonage(request):
    # Registra las credenciales para depuración (¡No hagas esto en producción!)
    logger.debug(f"API_KEY: {settings.OPENTOK_API_KEY}")
    logger.debug(f"API_SECRET: {settings.OPENTOK_API_SECRET}")

    # Inicializa OpenTok con la API key y secret desde settings
    opentok = OpenTok(settings.OPENTOK_API_KEY, settings.OPENTOK_API_SECRET)

    try:
        # Crear una sesión que utiliza el OpenTok Media Router
        session = opentok.create_session(
            media_mode=MediaModes.routed,
            archive_mode=ArchiveModes.manual
        )

        # Genera un token para la sesión
        token = opentok.generate_token(session.session_id, role=Roles.publisher)

        # Retorna el Session ID y Token como un JSON
        return JsonResponse({
            'apiKey': settings.OPENTOK_API_KEY,
            'sessionId': session.session_id,
            'token': token
        })
    except Exception as e:
        logger.error(f"Error al crear la sesión: {str(e)}")
        return JsonResponse({'error': 'Failed to create session', 'message': str(e)}, status=500)
