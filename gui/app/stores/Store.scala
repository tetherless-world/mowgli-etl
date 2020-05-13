package stores

import com.google.inject.ImplementedBy

@ImplementedBy(classOf[PlaceholderStore])
trait Store {
}
