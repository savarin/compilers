import format
import model


if __name__ == "__main__":
    program_1 = model.Print(model.Literal(42))
    print(format.format(program_1))
