"""
catho_parser.py
===============
Parser for Catho job listings using regular expressions.
Parses a single job text and saves the result as JSON in the ./data/ folder.

Extracted fields:
    job_title, contract_type, location, company, salary,
    posted_on, num_vacancies, schedule, area,
    requirements, differentials, whatsapp_contact, contract_via,
    contract_duration, diversity_profile, benefits,
    company_data, general_info
"""

import re
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    job_title: Optional[str] = None
    contract_type: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[str] = None
    posted_on: Optional[str] = None
    num_vacancies: Optional[str] = None
    schedule: Optional[str] = None
    area: Optional[str] = None
    requirements: list = field(default_factory=list)
    differentials: list = field(default_factory=list)
    whatsapp_contact: Optional[str] = None
    contract_via: Optional[str] = None
    contract_duration: Optional[str] = None
    diversity_profile: bool = False
    benefits: list = field(default_factory=list)
    company_data: Optional[str] = None
    general_info: Optional[str] = None


VALID_LOCATIONS = [
    r"Osasco", r"Vila\s+Campesina", r"Centro\s*[-–]\s*Osasco",
    r"Carapicuíba", r"Barueri", r"Jandira", r"Cotia",
    r"Santana\s+de\s+Parna[ií]ba", r"Itapevi", r"Alphaville",
]

_RE_LOCATION = re.compile(
    r"(" + "|".join(VALID_LOCATIONS) + r")[^,\n]*[-–,]?\s*(?:SP|São Paulo)?",
    re.IGNORECASE,
)


def _clean(text: str) -> str:
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_block(text: str, start: str, end: str) -> Optional[str]:
    pattern = re.compile(
        re.escape(start) + r"(.*?)" + re.escape(end),
        re.IGNORECASE | re.DOTALL,
    )
    m = pattern.search(text)
    return m.group(1).strip() if m else None


def extract_job_title(text: str) -> Optional[str]:
    m = re.search(r"Vaga\s+de\s+(.+?)(?:\n|\r|$)", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_contract_type(text: str) -> Optional[str]:
    m = re.search(
        r"Regime\s+de\s+Contrata[çc][aã]o\s*\n?\s*([A-Za-zÀ-ú ]+)",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).strip()
    m = re.search(
        r"\b(Est[áa]gio|Aprendiz|CLT|PJ|Temporário|Freelancer)\b",
        text, re.IGNORECASE
    )
    return m.group(1).capitalize() if m else None


def extract_location(text: str) -> Optional[str]:
    m = _RE_LOCATION.search(text)
    if not m:
        return None
    snippet = m.group(0).strip().rstrip(",")
    if not re.search(r"\bSP\b|São Paulo", snippet, re.IGNORECASE):
        context = text[max(0, m.start() - 5):m.start() + 60]
        if not re.search(r"\bSP\b|São Paulo", context, re.IGNORECASE):
            return None
    return snippet


def extract_company(text: str) -> Optional[str]:
    m = re.search(
        r"(?:Osasco|SP|São Paulo)\s*\(?[0-9]*\)?\s+"
        r"([A-ZÁÉÍÓÚÀÃÕ][A-ZÁÉÍÓÚÀÃÕA-Za-záéíóúàãõ ]{2,}"
        r"(?:\s+[A-ZÁÉÍÓÚÀÃÕ][A-Za-záéíóúàãõA-Z]*){0,5})",
        text
    )
    if m:
        candidate = m.group(1).strip()
        if len(candidate) > 4 and not re.match(r"^(Usar|Suas|Enviar|Menu)", candidate, re.IGNORECASE):
            return candidate
    block = _extract_block(text, "Dados da Empresa", "NACIONALIDADE")
    if block:
        line = block.strip().splitlines()[0].strip()
        if line:
            return line
    return None


def extract_salary(text: str) -> Optional[str]:
    all_matches = re.findall(
        r"R\$\s*[\d.,]+(?:\s*/\s*[\w]+)?(?:\s*[\+e]\s*[\w ]+)?",
        text, re.IGNORECASE
    )
    return max(all_matches, key=len).strip() if all_matches else None


def extract_posted_on(text: str) -> Optional[str]:
    m = re.search(
        r"Publicad[ao]\s+(?:em\s+)?(\d{1,2}/\d{1,2}|hoje)",
        text, re.IGNORECASE
    )
    return m.group(1).strip() if m else None


def extract_num_vacancies(text: str) -> Optional[str]:
    m = re.search(r"(\d+)\s+vaga[s]?", text, re.IGNORECASE)
    return m.group(1) if m else None


def extract_schedule(text: str) -> Optional[str]:
    m = re.search(
        r"(?:Escala|Horário|Carga hor[aá]ria)[:\s]+(.{5,80}?)(?:\n|$)",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).strip()
    m = re.search(
        r"(\d{1,2}[h:]\d{0,2}\s*[aà][o]?\s*\d{1,2}[h:]\d{0,2}(?:\s*[-–]\s*com\s+.+?)?)",
        text, re.IGNORECASE
    )
    return m.group(1).strip() if m else None


def extract_area(text: str) -> Optional[str]:
    m = re.search(r"[AÁ]rea\s+de\s+atua[çc][aã]o[:\s]+([^\n.]+)", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_requirements(text: str) -> list:
    block = _extract_block(text, "REQUISITOS", "DIFERENCIAL") or _extract_block(text, "REQUISITOS", "\n\n")
    if not block:
        return []
    return [r.strip() for r in re.split(r"\n|;", block) if r.strip()]


def extract_differentials(text: str) -> list:
    block = _extract_block(text, "DIFERENCIAL", "\n\n")
    if not block:
        return []
    return [d.strip() for d in re.split(r"\n|;", block) if d.strip()]


def extract_whatsapp(text: str) -> Optional[str]:
    m = re.search(r"whatsapp\s+([\d()\s\-]+)[-–]?\s*([A-Za-zÀ-ú]+)?", text, re.IGNORECASE)
    if m:
        number = m.group(1).strip()
        name = m.group(2).strip() if m.group(2) else ""
        return f"{number} — {name}".strip(" —") if name else number
    m = re.search(
        r"(?:enviar|curriculo|cv|contato)[^\n]{0,30}?([\d()\s\-]{10,20})\s*[-–]\s*([A-Za-zÀ-ú]+)",
        text, re.IGNORECASE
    )
    return f"{m.group(1).strip()} — {m.group(2).strip()}" if m else None


def extract_contract_via(text: str) -> Optional[str]:
    m = re.search(r"\b(Nube|CIEE|IEL|Integração)\b", text, re.IGNORECASE)
    return m.group(1) if m else None


def extract_contract_duration(text: str) -> Optional[str]:
    m = re.search(r"(?:contrato|prazo)\s+de\s+(\d+\s+(?:ano|m[eê]s)[s]?)", text, re.IGNORECASE)
    return m.group(1) if m else None


def extract_diversity_profile(text: str) -> bool:
    return bool(re.search(r"(vaga\s+aberta\s+para\s+todas|diversidade|inclus[aã]o)", text, re.IGNORECASE))


def extract_benefits(text: str) -> list:
    end_marker = r"(?:Regime\s+de\s+Contrata[çc][aã]o|Dados\s+da\s+Empresa|Horário\s+Informa[çc][oõ]es)"
    m = re.search(
        r"Benef[ií]cios\s*\n?\s*(.*?)\s*(?=" + end_marker + r")",
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        items = re.split(r",|\n|;", m.group(1))
        return [i.strip() for i in items if i.strip() and len(i.strip()) > 2]
    return []


def extract_company_data(text: str) -> Optional[str]:
    m = re.search(
        r"Dados\s+da\s+Empresa\s*\n(.*?)(?=\(D\s+Denunciar|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    return m.group(1).strip() if m else None


def extract_general_info(text: str) -> Optional[str]:
    m = re.search(
        r"o\s+Pular\s*\n(.*?)\n\s*(?:<\s*compartilhar|Benefícios|Horário\s+Informa)",
        text, re.IGNORECASE | re.DOTALL
    )
    return m.group(1).strip() if m else None


def parse_job(raw_text: str) -> Job:
    t = _clean(raw_text)
    return Job(
        job_title=extract_job_title(t),
        contract_type=extract_contract_type(t),
        location=extract_location(t),
        company=extract_company(t),
        salary=extract_salary(t),
        posted_on=extract_posted_on(t),
        num_vacancies=extract_num_vacancies(t),
        schedule=extract_schedule(t),
        area=extract_area(t),
        requirements=extract_requirements(t),
        differentials=extract_differentials(t),
        whatsapp_contact=extract_whatsapp(t),
        contract_via=extract_contract_via(t),
        contract_duration=extract_contract_duration(t),
        diversity_profile=extract_diversity_profile(t),
        benefits=extract_benefits(t),
        company_data=extract_company_data(t),
        general_info=extract_general_info(t),
    )


def save_job_parsed(job: Job, index = None , output_dir: str = "data/jobs") -> str:
    if index == None:
        pass
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%d-%m_%H-%M")
    job_name = re.sub(r"[^\w]", "_", job.job_title or "unknown")
    filename = f"{index}_{job_name}.json"
    filepath = os.path.join(output_dir, filename)
    payload = {"saved_at": timestamp, **asdict(job)}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return filepath


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            text = f.read()
    else:
       text = None

    job = parse_job(text)
    path = save_job_parsed(job)
    print(f"Saved → {path}")