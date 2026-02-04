# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/04 19:39:10 by mel-shdo          #+#    #+#              #
#    Updated: 2026/02/04 22:29:26 by mel-shdo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME	= push_swap
CC		= cc
CFLAGS	= -Wall -Werror -Wextra
SRCS	= push_swap.c parsing.c errors.c metrics.c \
		  stack_init.c stack_utils.c utils_lib.c \
		  swap.c push.c rotate.c reverse_rotate.c \
		  sort_simple.c sort_medium.c sort_complex.c \
		  sort_adaptive.c

OBJS	= $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
		$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o : %.c
		$(CC) $(CFLAGS) -c $< -o $@

clean:
		rm -f $(OBJS)

fclean: clean
		rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re