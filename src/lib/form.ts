export type ApplicationPayload = {
  prenom: string
  nom: string
  societe: string
  presence: string
  ca: string
  ville: string
  telephone: string
  email: string
  offre: string
  pourquoi: string
}

export async function submitApplication(data: ApplicationPayload) {
  const body = new URLSearchParams({
    'form-name': 'candidature',
    ...data,
  })

  const response = await fetch('/__forms.html', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  })

  if (!response.ok) {
    throw new Error(`Envoi refusé (${response.status})`)
  }
}
