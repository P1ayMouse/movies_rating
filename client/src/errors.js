// DRF errors look like {"detail": "..."}, {"detail": ["..."]} or {"username": ["..."]}
export async function errorMessage(response) {
  try {
    const data = await response.json();
    return [data.detail ?? Object.values(data)].flat(2)[0] || `Server error ${response.status}`;
  } catch {
    return `Server error ${response.status}`;
  }
}
