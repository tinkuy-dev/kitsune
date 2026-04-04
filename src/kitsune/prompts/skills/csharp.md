C# context:
- LINQ: first-class querying (collection.Where(x => x > 0).Select(x => x.Name))
- Async/Await: returns Task or Task<T>, gold standard for async
- Records: immutable reference types with value-based equality (C# 9+)
- Watch for: async void (crashes on exceptions), Task.Wait()/.Result (deadlocks), multiple IEnumerable enumeration
- Nullable reference types: enable in project for compile-time null safety
- Frameworks: ASP.NET Core (Minimal APIs, MVC, Blazor), Entity Framework Core
- Testing: xUnit, NUnit, Moq
