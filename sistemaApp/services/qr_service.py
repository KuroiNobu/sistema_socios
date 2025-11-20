"""Centralized QR generation helpers.

Este módulo crea un servicio reutilizable para generar códigos QR tanto para
credenciales como para descuentos, manteniendo una sola fuente de verdad.
"""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, Optional

import qrcode


@dataclass(frozen=True)
class QRConfig:
    box_size: int = 8
    border: int = 3
    fill_color: str = "black"
    back_color: str = "white"


@dataclass(frozen=True)
class QRResult:
    payload: Dict[str, Any]
    payload_json: str
    data_uri: str


class QRCodeService:
    """Small service responsible for turning payloads into QR data URIs."""

    def __init__(self, config: Optional[QRConfig] = None) -> None:
        self._config = config or QRConfig()

    def generate(self, payload: Dict[str, Any]) -> QRResult:
        sanitized_payload = {k: v for k, v in payload.items() if v not in (None, "")}
        payload_json = json.dumps(sanitized_payload, ensure_ascii=False)

        qr = qrcode.QRCode(box_size=self._config.box_size, border=self._config.border)
        qr.add_data(payload_json)
        qr.make(fit=True)
        image = qr.make_image(fill_color=self._config.fill_color, back_color=self._config.back_color)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")

        return QRResult(
            payload=sanitized_payload,
            payload_json=payload_json,
            data_uri=f"data:image/png;base64,{encoded}",
        )


def generate_credential_qr(credencial) -> QRResult:
    socio = credencial.id_socio
    payload = {
        "type": "credential",
        "credential_id": credencial.pk,
        "socio_id": socio.pk if socio else None,
        "nombre": getattr(socio, "nombre", ""),
        "apellido": getattr(socio, "apellido", ""),
        "email": getattr(socio, "email", ""),
        "codigo": credencial.codigo_qr,
    }
    return QRCodeService(QRConfig(box_size=8, border=3)).generate(payload)


def generate_discount_qr(descuento) -> QRResult:
    proveedor = getattr(descuento, "proveedor", None)
    payload = {
        "type": "discount",
        "discount_id": descuento.pk,
        "codigo": descuento.codigo_qr,
        "descripcion": descuento.descripcion,
        "proveedor": getattr(proveedor, "nombre", ""),
        "proveedor_id": getattr(proveedor, "id_proveedor", None),
    }
    return QRCodeService(QRConfig(box_size=6, border=2)).generate(payload)


def generate_custom_qr(payload: Dict[str, Any], config: Optional[QRConfig] = None) -> QRResult:
    return QRCodeService(config).generate(payload)
