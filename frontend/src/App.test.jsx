import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders Encrypt a String header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Encrypt a String/i);
  expect(headerElement).toBeInTheDocument();
});

test('encrypts text', async () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Enter text to encrypt/i);
  const buttonElement = screen.getByText(/Encrypt/i);

  fireEvent.change(inputElement, { target: { value: 'Hello world' } });
  fireEvent.click(buttonElement);

  const cipherElement = await screen.findByText(/Cipher:/i);
  const ivElement = await screen.findByText(/IV:/i);

  expect(cipherElement).toBeInTheDocument();
  expect(ivElement).toBeInTheDocument();
});
