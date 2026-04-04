PHP context:
- Traits: horizontal code reuse for single inheritance limitation
- Magic Methods: __get, __set, __call, __construct intercept calls
- Dependency Injection: constructor injection (modern frameworks)
- Watch for: loose typing (== vs ===, always use strict), missing declare(strict_types=1), SQL injection via string concat (use PDO prepared statements)
- Namespaces and autoloading via Composer (PSR-4)
- Frameworks: Laravel (Eloquent ORM, Blade), Symfony (enterprise, decoupled)
- Testing: PHPUnit, Pest
