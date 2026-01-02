# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/30 21:04:38 by mel-shdo          #+#    #+#              #
#    Updated: 2025/12/31 21:42:15 by mel-shdo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		= libftprintf.a
CC			= cc
CFLAGS		= -Wall -Wextra -Werror -fPIC
AR			= ar rcs
RM			= rm -f

LIBFT_DIR	= ./libft
LIBFT		= $(LIBFT_DIR)/libft.a

SRCS		= ft_printf.c \
			  ft_print_cs.c \
			  ft_print_id.c \
			  ft_print_ux.c \
			  ft_print_ptr.c

OBJS		= $(SRCS:.c=.o)

all:		$(NAME)

$(NAME):	$(LIBFT) $(OBJS)
						cp $(LIBFT) $(NAME)
						$(AR) $(NAME) $(OBJS)

$(LIBFT):
			make -C $(LIBFT_DIR)
%.o: %.c
			$(CC) $(CFLAGS) -I ./libft -c $< -o $@

clean:
			$(RM) $(OBJS)
			make -C $(LIBFT_DIR) clean

fclean:		clean
			$(RM) $(NAME)
			make -C $(LIBFT_DIR) fclean

re:			fclean all

.PHONY:		all clean fclean re