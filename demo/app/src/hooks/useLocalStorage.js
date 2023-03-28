import React from 'react'

/**
 * hook for setting and getting values form local browser storage
 *
 * @param {string} key - identifies which value to set or retrieve
 * @param {string} initialValue - starting value if no value is stored
 */
const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = React.useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item
        ? JSON.parse(item)
        : initialValue
    } catch (error) {
      return initialValue
    }
  })

  const setValue = (value) => {
    try {
      const valueToStore = typeof value === 'function'
        ? value(storedValue)
        : value

      // save to the state
      setStoredValue(valueToStore)

      // save to localStorage
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.log(error)
    }
  }

  return [storedValue, setValue]
}

export default useLocalStorage
