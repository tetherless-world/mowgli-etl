package stores

import com.google.inject.ImplementedBy
import io.github.tetherlessworld.dsa_models.policy.{Policy, PolicyId}

@ImplementedBy(classOf[PlaceholderStore])
trait Store {
}
