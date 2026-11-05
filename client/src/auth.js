import { reactive } from 'vue'

const ACCESS_KEY = 'movies_rating-access'
const REFRESH_KEY = 'movies_rating-refresh'

export const authState = reactive({ user: null, loaded: false, error: null })

export function saveTokens({ access, refresh }) {
  localStorage.setItem(ACCESS_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
  authState.user = null
}

function request(url, options) {
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
      'Authorization': `Bearer ${localStorage.getItem(ACCESS_KEY)}`,
    },
  })
}

async function refreshAccessToken() {
  const response = await fetch('/api/v1/auth/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: localStorage.getItem(REFRESH_KEY) }),
  })
  if (response.status !== 200) {
    return false
  }
  localStorage.setItem(ACCESS_KEY, (await response.json()).access)
  return true
}

export async function authFetch(url, options = {}) {
  const response = await request(url, options)
  if (response.status !== 403) {
    return response
  }
  if (!(await refreshAccessToken())) {
    clearTokens()
    return response
  }
  return request(url, options)
}

export async function loadCurrentUser() {
  authState.error = null
  try {
    const response = await authFetch('/api/v1/auth/user-info/')
    if (response.status === 200) {
      authState.user = await response.json()
    } else if (response.status === 403) {
      authState.user = null
    } else {
      authState.error = `Server error ${response.status}`
    }
  } catch {
    authState.error = 'Network error'
  }
  authState.loaded = true
  return authState.user
}
