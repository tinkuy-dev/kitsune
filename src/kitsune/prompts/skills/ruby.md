Ruby context:
- Blocks, Procs, Lambdas: passing code chunks (array.each { |item| puts item })
- Metaprogramming: define_method, method_missing — powerful but hard to debug
- Mixins: module + include/extend for shared behavior instead of multiple inheritance
- Watch for: NoMethodError on nil (use safe navigation &.), mutable default args, magic code
- Everything is an object, including numbers and nil
- Frameworks: Ruby on Rails (MVC, Active Record), Sinatra (micro)
- Testing: RSpec (BDD), Minitest. Background: Sidekiq
