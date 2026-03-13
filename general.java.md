# Spring Boot Web App — General Architecture Rules & Design Guidelines
> Drop this file into any coding agent prompt. It defines the non-negotiable rules for building
> any Spring Boot CRUD web application. The business domain changes; these rules never do.
> Targets: Java 17, Spring Boot 3.1.x — safe for models with knowledge cutoff at October 2023.

---

## 1. Stack Baseline

| Concern | Technology | Notes |
|---|---|---|
| Language | Java 17 | Use records, sealed classes, text blocks where appropriate |
| Framework | Spring Boot 3.1.x | Always use `spring-boot-starter-parent` as parent POM |
| UI | Thymeleaf + Bootstrap 5 (CDN) | No JS frameworks. No local asset pipeline. |
| Build | Maven (pre-installed) | Do not use Gradle unless explicitly asked |
| DB — dev profile | H2 in-memory | Console enabled at `/h2-console` |
| DB — prod profile | PostgreSQL | Config via env vars only, never hardcoded credentials |
| Security | Spring Security 6 | In-memory user unless otherwise specified |
| Validation | Bean Validation (`jakarta.validation`) | Always validate at controller boundary |
| Testing | JUnit 5 + Mockito + Spring Boot Test | TDD — tests alongside or before code |

---

## 2. Maven `pom.xml` — Required Dependencies

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.1.5</version>
</parent>

<properties>
    <java.version>17</java.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    <dependency>
        <groupId>org.thymeleaf.extras</groupId>
        <artifactId>thymeleaf-extras-springsecurity6</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

---

## 3. Project Structure (Clean Architecture + DDD)

Every project must follow this exact package layout.
Replace `{appname}` and `{entity}` with actual names.

```
src/main/java/com/example/{appname}/
│
├── domain/
│   ├── model/              # Pure Java: Entities, Value Objects, Enums
│   └── repository/         # Java interfaces only — zero Spring/JPA annotations
│
├── application/
│   └── service/            # One service class per aggregate root
│                           # Depends only on domain interfaces
│
├── infrastructure/
│   ├── persistence/        # JPA @Entity classes + Spring Data repo implementations
│   └── security/           # SecurityConfig, UserDetailsService if custom
│
└── presentation/
    └── web/                # @Controller classes, one per aggregate root
                            # Thin — zero business logic here

src/main/resources/
├── application.yml
├── application-dev.yml
├── application-prod.yml
└── templates/
    ├── layout.html              # Shared Thymeleaf layout fragment (navbar, flash msgs)
    ├── dashboard.html
    └── {entity}/
        ├── list.html
        ├── form.html            # Reused for both create AND edit
        └── confirm-delete.html

src/test/java/com/example/{appname}/
├── domain/                      # Pure unit tests — no Spring context loaded
├── application/                 # Unit tests with Mockito mocks
├── infrastructure/              # @DataJpaTest — H2
└── presentation/                # @WebMvcTest — MockMvc
```

---

## 4. Layering Rules — Non-Negotiable

| Rule | Description |
|---|---|
| **Domain is pure Java** | Zero `@Entity`, zero `@Repository`, zero Spring imports in `domain/` |
| **Services use interfaces** | Application services inject domain repository interfaces, never JPA repos directly |
| **Infrastructure adapts** | JPA repos in `infrastructure/` implement domain interfaces |
| **Controllers are thin** | No `if/else` business logic in controllers. Call service, redirect, done. |
| **One-way dependency** | Outer layers depend on inner layers. Inner layers never import from outer layers. |
| **No service calls from templates** | Thymeleaf templates only render model attributes put there by the controller |

### Visual Dependency Direction

```
presentation  →  application  →  domain
infrastructure →  domain
```
Infrastructure and Presentation both point inward. Domain has no outward arrows.

---

## 5. Domain Model Rules

### Entities

```java
// ✅ Correct — pure domain entity, no framework imports
public class Product {
    private UUID id;

    @NotBlank
    private String name;

    private Money price;
    private ProductStatus status;

    public void discontinue() {
        if (this.status == ProductStatus.DISCONTINUED)
            throw new DomainException("Product is already discontinued");
        this.status = ProductStatus.DISCONTINUED;
    }
}
```

```java
// ❌ Wrong — JPA leaking into domain layer
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue
    private Long id;
    ...
}
```

### ID Strategy
- Always use `UUID` for entity IDs in the domain layer.
- Generate IDs in the domain constructor: `this.id = UUID.randomUUID()`.
- The JPA `@Entity` in `infrastructure/` maps UUID to the DB column.

### Value Objects
Wrap primitives when they carry business meaning:

```java
// Value object example
public record Email(String value) {
    public Email {
        if (value == null || !value.contains("@"))
            throw new DomainException("Invalid email: " + value);
    }
}
```

### Enums
Use Java enums for all finite state sets. Always define them in `domain/model/`:

```java
public enum TaskStatus { TODO, IN_PROGRESS, IN_REVIEW, DONE, CANCELLED }
public enum UserRole  { ADMIN, MANAGER, DEVELOPER, VIEWER }
```

### Domain Exceptions
Define a base `DomainException` (unchecked) in `domain/model/`:

```java
public class DomainException extends RuntimeException {
    public DomainException(String message) { super(message); }
}
```

---

## 6. Repository Interface Pattern

```java
// domain/repository/ProductRepository.java — pure Java interface
public interface ProductRepository {
    Product save(Product product);
    Optional<Product> findById(UUID id);
    List<Product> findAll();
    void deleteById(UUID id);
    boolean existsByName(String name);
}
```

```java
// infrastructure/persistence/JpaProductRepository.java — Spring Data
public interface JpaProductRepository extends JpaRepository<ProductJpaEntity, UUID> {
    boolean existsByName(String name);
}
```

```java
// infrastructure/persistence/ProductRepositoryAdapter.java — adapter/bridge
@Repository
@RequiredArgsConstructor
public class ProductRepositoryAdapter implements ProductRepository {

    private final JpaProductRepository jpa;
    private final ProductMapper mapper;

    @Override
    public Product save(Product product) {
        return mapper.toDomain(jpa.save(mapper.toJpa(product)));
    }

    @Override
    public Optional<Product> findById(UUID id) {
        return jpa.findById(id).map(mapper::toDomain);
    }
    // ... other methods
}
```

---

## 7. Application Service Rules

```java
@Service
@Transactional
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository; // domain interface, NOT JPA repo

    public Product create(CreateProductCommand cmd) {
        if (productRepository.existsByName(cmd.name()))
            throw new DomainException("A product with this name already exists");

        Product product = new Product(cmd.name(), cmd.price());
        return productRepository.save(product);
    }

    public void delete(UUID id) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Product not found: " + id));
        productRepository.deleteById(product.getId());
    }
}
```

**Command Objects** — Use Java records as input DTOs for write operations:

```java
public record CreateProductCommand(
    @NotBlank String name,
    @NotNull BigDecimal price
) {}
```

---

## 8. Controller Rules

```java
@Controller
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("products", productService.findAll());
        return "products/list";
    }

    @GetMapping("/new")
    public String showCreateForm(Model model) {
        model.addAttribute("form", new ProductForm());
        return "products/form";
    }

    @PostMapping
    public String create(@Valid @ModelAttribute("form") ProductForm form,
                         BindingResult result,
                         RedirectAttributes flash) {
        if (result.hasErrors()) return "products/form";
        productService.create(form.toCommand());
        flash.addFlashAttribute("success", "Product created successfully.");
        return "redirect:/products";
    }

    @GetMapping("/{id}/edit")
    public String showEditForm(@PathVariable UUID id, Model model) {
        Product p = productService.findById(id);
        model.addAttribute("form", ProductForm.from(p));
        model.addAttribute("productId", id);
        return "products/form";
    }

    @PostMapping("/{id}")
    public String update(@PathVariable UUID id,
                         @Valid @ModelAttribute("form") ProductForm form,
                         BindingResult result,
                         RedirectAttributes flash) {
        if (result.hasErrors()) return "products/form";
        productService.update(id, form.toCommand());
        flash.addFlashAttribute("success", "Product updated.");
        return "redirect:/products";
    }

    @PostMapping("/{id}/delete")
    public String delete(@PathVariable UUID id, RedirectAttributes flash) {
        productService.delete(id);
        flash.addFlashAttribute("success", "Product deleted.");
        return "redirect:/products";
    }
}
```

**Rules:**
- Always use `redirect:/` after POST (PRG pattern — Post/Redirect/Get).
- Use `RedirectAttributes` for flash messages, never query params.
- Validate with `@Valid` + `BindingResult` — return the form view on errors.
- Delete operations use `POST` (HTML forms don't support `DELETE`), not `@DeleteMapping`.

---

## 9. Form / DTO Objects

```java
// presentation/web/product/ProductForm.java
public class ProductForm {

    @NotBlank(message = "Name is required")
    private String name;

    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Price must be positive")
    private BigDecimal price;

    // Factory method from domain entity
    public static ProductForm from(Product p) {
        ProductForm f = new ProductForm();
        f.name = p.getName();
        f.price = p.getPrice().amount();
        return f;
    }

    // Convert to application command
    public CreateProductCommand toCommand() {
        return new CreateProductCommand(this.name, this.price);
    }

    // getters + setters required by Thymeleaf binding
}
```

---

## 10. Configuration Files

### `application.yml`
```yaml
server:
  port: 8765

spring:
  profiles:
    active: dev
  thymeleaf:
    cache: false
```

### `application-dev.yml`
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:appdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
    driver-class-name: org.h2.Driver
    username: sa
    password:
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        format_sql: true
  h2:
    console:
      enabled: true
      path: /h2-console
```

### `application-prod.yml`
```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASS}
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    database-platform: org.hibernate.dialect.PostgreSQLDialect
    show-sql: false
```

---

## 11. Security Configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login", "/css/**", "/js/**", "/h2-console/**").permitAll()
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/", true)
                .permitAll()
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login?logout")
                .permitAll()
            )
            .csrf(csrf -> csrf
                .ignoringRequestMatchers("/h2-console/**") // H2 console needs this
            )
            .headers(headers -> headers
                .frameOptions().sameOrigin() // H2 console uses iframes
            );
        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user = User.withDefaultPasswordEncoder()
            .username("demo")
            .password("demo")
            .roles("USER")
            .build();
        return new InMemoryUserDetailsManager(user);
    }
}
```

---

## 12. Thymeleaf Templates

### `layout.html` — Shared Fragment
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org"
      xmlns:sec="http://www.thymeleaf.org/extras/spring-security">
<head th:fragment="head(title)">
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title th:text="${title}">App</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"/>
</head>
<body>
<nav th:fragment="navbar" class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">App</a>
        <div class="navbar-nav ms-auto" sec:authorize="isAuthenticated()">
            <a class="nav-link" href="/">Dashboard</a>
            <!-- add entity links here -->
            <a class="nav-link" th:href="@{/logout}"
               onclick="event.preventDefault();
                        document.getElementById('logout-form').submit();">Logout</a>
            <form id="logout-form" th:action="@{/logout}" method="post" hidden></form>
        </div>
    </div>
</nav>

<div th:fragment="flash" class="container">
    <div th:if="${success}" class="alert alert-success" th:text="${success}"></div>
    <div th:if="${error}"   class="alert alert-danger"  th:text="${error}"></div>
</div>
</body>
</html>
```

### Form Template Pattern
```html
<!-- Always reuse one form.html for create AND edit -->
<!-- Detect mode by checking if entity ID is null -->
<form th:action="${entityId != null} ? @{/products/{id}(id=${entityId})} : @{/products}"
      th:object="${form}" method="post">
    <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>

    <div class="mb-3">
        <label class="form-label">Name</label>
        <input type="text" th:field="*{name}"
               th:classappend="${#fields.hasErrors('name')} ? 'is-invalid'" class="form-control"/>
        <div class="invalid-feedback" th:errors="*{name}"></div>
    </div>

    <button type="submit" class="btn btn-primary"
            th:text="${entityId != null} ? 'Update' : 'Create'">Save</button>
    <a th:href="@{/products}" class="btn btn-secondary">Cancel</a>
</form>
```

---

## 13. TDD Test Patterns

### Unit Test — Domain (no Spring)
```java
class ProductTest {
    @Test
    void shouldThrowWhenDiscontinuingAlreadyDiscontinuedProduct() {
        Product p = new Product("Widget", new Money(BigDecimal.TEN));
        p.discontinue();
        assertThrows(DomainException.class, p::discontinue);
    }
}
```

### Unit Test — Service (Mockito)
```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock ProductRepository productRepository;
    @InjectMocks ProductService productService;

    @Test
    void shouldThrowWhenCreatingDuplicateName() {
        given(productRepository.existsByName("Widget")).willReturn(true);
        assertThrows(DomainException.class,
            () -> productService.create(new CreateProductCommand("Widget", BigDecimal.TEN)));
    }
}
```

### Integration Test — Repository
```java
@DataJpaTest
class ProductRepositoryAdapterTest {

    @Autowired TestEntityManager em;
    @Autowired JpaProductRepository jpa;

    @Test
    void shouldFindByName() {
        em.persist(new ProductJpaEntity(UUID.randomUUID(), "Widget", BigDecimal.TEN));
        assertTrue(jpa.existsByName("Widget"));
    }
}
```

### Web Test — Controller
```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {

    @Autowired MockMvc mvc;
    @MockBean ProductService productService;

    @Test
    @WithMockUser
    void shouldRenderListPage() throws Exception {
        given(productService.findAll()).willReturn(List.of());
        mvc.perform(get("/products"))
           .andExpect(status().isOk())
           .andExpect(view().name("products/list"));
    }

    @Test
    @WithMockUser
    void shouldRedirectAfterCreate() throws Exception {
        mvc.perform(post("/products").with(csrf())
               .param("name", "Widget")
               .param("price", "9.99"))
           .andExpect(status().is3xxRedirection())
           .andExpect(redirectedUrl("/products"));
    }
}
```

---

## 14. Exception Handling

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public String handleNotFound(EntityNotFoundException ex, Model model) {
        model.addAttribute("error", ex.getMessage());
        return "error/404";
    }

    @ExceptionHandler(DomainException.class)
    public String handleDomain(DomainException ex, RedirectAttributes flash,
                                HttpServletRequest request) {
        flash.addFlashAttribute("error", ex.getMessage());
        String referer = request.getHeader("Referer");
        return "redirect:" + (referer != null ? referer : "/");
    }
}
```

---

## 15. Checklist — Before Considering Any CRUD App Done

### Architecture
- [ ] Domain layer has zero Spring / JPA / framework imports
- [ ] Application services inject domain repository interfaces (not JPA repos)
- [ ] Infrastructure adapters implement domain interfaces
- [ ] Controllers are thin — no business logic, only call services and redirect

### Features
- [ ] Login page at `/login`, all other routes protected
- [ ] Full CRUD for every entity (list, create, edit, delete)
- [ ] Confirmation step before delete
- [ ] Cascades / orphan behavior explicitly defined (no silent data loss)
- [ ] All forms validate server-side with inline error messages
- [ ] Flash messages on success and error after redirects
- [ ] Dashboard with summary counts

### Config
- [ ] App runs on the specified port (default 8765 unless told otherwise)
- [ ] Dev profile uses H2 — no external DB required to run
- [ ] Prod profile reads DB config from env vars only
- [ ] `mvn spring-boot:run` starts with zero errors

### Tests
- [ ] Domain unit tests (no Spring context)
- [ ] Service unit tests (Mockito)
- [ ] Controller tests (`@WebMvcTest`)
- [ ] Repository tests (`@DataJpaTest`)
- [ ] `mvn test` passes with zero failures

---

## 16. Common Mistakes to Avoid

| Mistake | Correct Approach |
|---|---|
| Putting `@Entity` in domain layer | Keep JPA entities in `infrastructure/persistence/` only |
| Calling JPA repos from controllers | Always go through the application service |
| Using `@Autowired` field injection | Use constructor injection (`@RequiredArgsConstructor` or explicit constructor) |
| Hardcoding DB credentials | Use `${ENV_VAR}` in `application-prod.yml` |
| Using `@ResponseBody` in a Thymeleaf controller | Use `@Controller`, not `@RestController` |
| Delete with `@GetMapping` | Delete must be `POST` (HTML forms don't support DELETE) |
| Business logic in templates | Put logic in services, put results in model attributes |
| Forgetting CSRF token in forms | Every POST form needs `th:action` (auto-includes CSRF) or explicit hidden field |
| Auto-increment Long IDs in domain | Use `UUID` in domain; map to DB sequence in JPA entity if needed |
| Returning entity directly from controller | Always use Form/DTO objects as the model attribute |
