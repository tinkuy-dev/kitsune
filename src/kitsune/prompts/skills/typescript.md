TypeScript context:
- Discriminated Unions: common literal property (e.g., `type: 'success' | 'error'`) to narrow types safely
- Mapped Types & Utility Types: Partial<T>, Pick<T, K>, Omit<T, K>, Record<K, T>
- Generics: reusable functions/classes <T> without losing type safety
- Watch for: `any` virus (prefer `unknown`), type assertions (`as T`) hiding bugs, optional chaining masking missing logic
- Async/Await returns Promise<T>, error handling with try/catch
- Frameworks: NestJS (backend), React/Next.js (TSX), Vue 3, Angular
- Tools: Zod (runtime validation), tRPC (E2E types)
