"""Correo transaccional desacoplado con soporte SendGrid."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from core.config import get_settings

try:
    from sendgrid import SendGridAPIClient  # type: ignore
    from sendgrid.helpers.mail import Email, From, Mail, To  # type: ignore
except Exception:  # pragma: no cover
    SendGridAPIClient = None  # type: ignore
    Email = None  # type: ignore
    From = None  # type: ignore
    Mail = None  # type: ignore
    To = None  # type: ignore


logger = logging.getLogger("optiferre.mail")


@dataclass(frozen=True)
class MailResult:
    ok: bool
    provider: str
    reason: str


def _wrap_html(title: str, intro: str, bullets: list[str], closing: str) -> str:
    bullet_html = "".join(f"<li style='margin:0 0 8px 0'>{item}</li>" for item in bullets)
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f4f8fc;padding:24px;color:#102c49;">
      <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:18px;padding:28px;border:1px solid #d8e6f3;">
        <div style="display:inline-block;padding:6px 12px;border-radius:999px;background:#e6f8fa;color:#0a7a89;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;">Nexus Pro</div>
        <h1 style="font-size:30px;line-height:1.05;margin:16px 0 12px 0;color:#102c49;">{title}</h1>
        <p style="font-size:16px;line-height:1.65;margin:0 0 16px 0;color:#24486e;">{intro}</p>
        <ul style="padding-left:18px;margin:0 0 18px 0;color:#24486e;font-size:15px;line-height:1.6;">{bullet_html}</ul>
        <p style="font-size:15px;line-height:1.65;margin:0;color:#24486e;">{closing}</p>
      </div>
    </div>
    """


def _send_email(to_email: str, subject: str, html_content: str) -> MailResult:
    settings = get_settings()
    if not settings.mail_enabled:
        return MailResult(False, settings.mail_provider, "mail_not_configured")
    if SendGridAPIClient is None or Mail is None or From is None or To is None:
        return MailResult(False, settings.mail_provider, "sendgrid_package_missing")

    try:
        message = Mail(
            from_email=From(settings.mail_from_email, settings.mail_from_name),
            to_emails=To(to_email),
            subject=subject,
            html_content=html_content,
        )
        if settings.mail_reply_to and Email is not None:
            message.reply_to = Email(settings.mail_reply_to)

        client = SendGridAPIClient(settings.sendgrid_api_key)
        response = client.send(message)
        logger.info("transactional_email_sent", extra={"to_email": to_email, "status_code": response.status_code})
        return MailResult(True, settings.mail_provider, f"status_{response.status_code}")
    except Exception:
        logger.exception("transactional_email_error", extra={"to_email": to_email, "subject": subject})
        return MailResult(False, settings.mail_provider, "send_failed")


def send_account_created_email(to_email: str, full_name: str, company_name: str) -> MailResult:
    html = _wrap_html(
        title="Tu cuenta fue creada correctamente",
        intro=f"{full_name}, ya quedó activo el acceso inicial para {company_name}. Desde ahora puedes entrar, cargar archivos y empezar a ver decisiones accionables de inventario.",
        bullets=[
            "Tu prueba guiada de 14 días ya está disponible.",
            "Puedes revisar capital inmovilizado, quiebres y compra sugerida.",
            "No necesitas una integración compleja para empezar.",
        ],
        closing="Entra a Nexus Pro y convierte tus archivos en una conversación clara de caja, abastecimiento y retorno.",
    )
    return _send_email(to_email, "Nexus Pro | Cuenta creada y prueba activada", html)


def send_login_notice_email(to_email: str, full_name: str, company_name: str) -> MailResult:
    html = _wrap_html(
        title="Ingresaste correctamente",
        intro=f"{full_name}, detectamos un inicio de sesión exitoso en {company_name}.",
        bullets=[
            "Ya puedes revisar tu dashboard y continuar el análisis.",
            "Si este acceso no fue tuyo, cambia la contraseña cuanto antes.",
            "Mantén tus credenciales bajo control para proteger la información del negocio.",
        ],
        closing="Este aviso busca darte trazabilidad y confianza sobre el uso de tu cuenta.",
    )
    return _send_email(to_email, "Nexus Pro | Inicio de sesión confirmado", html)


def send_subscription_status_email(to_email: str, company_name: str, plan_name: str, status: str) -> MailResult:
    html = _wrap_html(
        title="Tu estado de suscripción fue actualizado",
        intro=f"La cuenta de {company_name} quedó asociada al plan {plan_name} con estado {status}.",
        bullets=[
            "El acceso y las capacidades activas dependen de este estado.",
            "Puedes seguir operando y revisar el valor entregado por el diagnóstico.",
            "Si necesitas soporte o una evolución más avanzada, puedes responder este correo.",
        ],
        closing="Gracias por seguir construyendo un proceso de inventario más claro, accionable y rentable.",
    )
    return _send_email(to_email, f"Nexus Pro | Suscripción {status}", html)


def send_support_ticket_created_to_customer(to_email: str, requester_name: str, ticket_id: int, subject: str) -> MailResult:
    html = _wrap_html(
        title="Recibimos tu solicitud de ayuda",
        intro=f"{requester_name}, tu solicitud fue registrada correctamente con el ticket #{ticket_id}.",
        bullets=[
            f"Asunto registrado: {subject}",
            "Tu mensaje ya quedó enviado al equipo de soporte.",
            "Te responderemos por correo al mismo email con el que abriste el caso.",
        ],
        closing="Gracias por escribirnos. Queremos que tu operación en Nexus Pro sea clara, estable y bien acompañada.",
    )
    return _send_email(to_email, f"Nexus Pro | Ticket #{ticket_id} recibido", html)


def send_support_ticket_created_to_operator(
    to_email: str,
    ticket_id: int,
    requester_name: str,
    requester_email: str,
    subject: str,
    body: str,
    company_name: str | None = None,
) -> MailResult:
    company_line = company_name or "No informada"
    html = _wrap_html(
        title=f"Nuevo ticket #{ticket_id}",
        intro=f"{requester_name} abrió un ticket desde Nexus Pro.",
        bullets=[
            f"Email: {requester_email}",
            f"Empresa: {company_line}",
            f"Asunto: {subject}",
            f"Mensaje inicial: {body}",
        ],
        closing="Revisa el caso y responde al cliente desde el canal operativo definido.",
    )
    return _send_email(to_email, f"Nexus Pro | Nuevo ticket #{ticket_id}", html)


def send_support_ticket_reply_to_customer(
    to_email: str,
    requester_name: str,
    ticket_id: int,
    subject: str,
    reply_body: str,
) -> MailResult:
    html = _wrap_html(
        title=f"Actualización de tu ticket #{ticket_id}",
        intro=f"{requester_name}, tu caso sobre '{subject}' tuvo una actualización.",
        bullets=[reply_body],
        closing="Si necesitas ampliar información, responde este correo o vuelve a tu espacio en Nexus Pro.",
    )
    return _send_email(to_email, f"Nexus Pro | Respuesta ticket #{ticket_id}", html)