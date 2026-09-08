import { useState, type FormEvent } from 'react'
import { submitApplication } from '../lib/form'
import { navigate } from '../lib/path'

const empty = {
  prenom: '',
  nom: '',
  societe: '',
  presence: '',
  ca: '',
  ville: '',
  telephone: '',
  email: '',
  offre: 'Saison',
  pourquoi: '',
  'bot-field': '',
}

export function ApplyForm() {
  const [data, setData] = useState(empty)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (data['bot-field']) return
    setPending(true)
    setError('')
    try {
      const { 'bot-field': _honeypot, ...payload } = data
      void _honeypot
      await submitApplication(payload)
      navigate('/merci')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Envoi impossible')
    } finally {
      setPending(false)
    }
  }

  const set =
    (key: keyof typeof empty) =>
    (event: { target: { value: string } }) =>
      setData((prev) => ({ ...prev, [key]: event.target.value }))

  return (
    <form className="form" name="candidature" method="POST" onSubmit={onSubmit}>
      <input type="hidden" name="form-name" value="candidature" />
      <label className="honeypot">
        Ne pas remplir
        <input name="bot-field" value={data['bot-field']} onChange={set('bot-field')} />
      </label>
      <div className="grid-2">
        <label>
          Prénom
          <input required name="prenom" value={data.prenom} onChange={set('prenom')} />
        </label>
        <label>
          Nom
          <input required name="nom" value={data.nom} onChange={set('nom')} />
        </label>
      </div>
      <label>
        Société
        <input required name="societe" value={data.societe} onChange={set('societe')} />
      </label>
      <label>
        Site, Instagram ou LinkedIn
        <input
          required
          name="presence"
          placeholder="https://"
          value={data.presence}
          onChange={set('presence')}
        />
      </label>
      <div className="grid-2">
        <label>
          CA annuel
          <select required name="ca" value={data.ca} onChange={set('ca')}>
            <option value="">Choisir</option>
            <option value="<200k">Moins de 200 k€ — trop tôt</option>
            <option value="200-500k">200–500 k€</option>
            <option value="500k-2m">500 k€–2 M€</option>
            <option value="2m+">Plus de 2 M€</option>
          </select>
        </label>
        <label>
          Offre
          <select name="offre" value={data.offre} onChange={set('offre')}>
            <option>Pilote</option>
            <option>Saison</option>
            <option>Empire</option>
          </select>
        </label>
      </div>
      <div className="grid-2">
        <label>
          Ville
          <input required name="ville" value={data.ville} onChange={set('ville')} />
        </label>
        <label>
          Téléphone
          <input required name="telephone" value={data.telephone} onChange={set('telephone')} />
        </label>
      </div>
      <label>
        Email
        <input required type="email" name="email" value={data.email} onChange={set('email')} />
      </label>
      <label>
        Pourquoi maintenant
        <textarea
          required
          name="pourquoi"
          value={data.pourquoi}
          onChange={set('pourquoi')}
          placeholder="Quel résultat d'affaires vous voulez dans 90 jours ?"
        />
      </label>
      {error ? <p className="warn">{error}</p> : null}
      <button className="btn" type="submit" disabled={pending}>
        {pending ? 'Envoi…' : 'Demander une place'}
      </button>
    </form>
  )
}
