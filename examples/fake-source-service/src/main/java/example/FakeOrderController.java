package example;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/orders")
class FakeOrderController {

    @GetMapping("/{orderId}")
    FakeOrderResponse getOrder(@PathVariable String orderId) {
        return new FakeOrderResponse(orderId, "pending");
    }

    @PostMapping
    FakeOrderResponse createOrder(@RequestBody FakeOrderRequest request) {
        return new FakeOrderResponse(request.reference(), "created");
    }
}

@Component
class FakeOrderExportJob {

    @Scheduled(cron = "0 0 * * * *")
    void exportOrders() {
        // Fake public example only.
    }
}

record FakeOrderRequest(String reference) {
}

record FakeOrderResponse(String orderId, String status) {
}
