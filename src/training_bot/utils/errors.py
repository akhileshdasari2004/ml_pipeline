class TrainingDataBotError(Exception):
    """Base exception for Training Data Bot."""
    pass

class LoadError(TrainingDataBotError):
    """Raised when document loading fails."""
    pass

class ProcessError(TrainingDataBotError):
    """Raised when text processing fails."""
    pass

class GenerationError(TrainingDataBotError):
    """Raised when AI generation fails."""
    pass

class QualityError(TrainingDataBotError):
    """Raised when quality evaluation fails."""
    pass

class ExportError(TrainingDataBotError):
    """Raised when data export fails."""
    pass

class ConfigurationError(TrainingDataBotError):
    """Raised when there is a configuration issue."""
    pass
